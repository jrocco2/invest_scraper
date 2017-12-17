import dataset
import pandas as pd
import redis
from invest_scrape.settings import *


class DatabaseComponents:

    def __init__(self, table_name, publish_name):
        """
        Initializes the database connection and redis server.
        """

        # Initialise Redis
        self.redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        # Initialise Database
        self.db = dataset.connect(POSTGRES_DB_URL)

        self.table_name = table_name  # Postgres table name
        self.publish_name = publish_name  # Redis publish name

    def update_transaction(self, item, new_dict, old_dict, table):
        """
        Check for differences between the items scraped and the row in the DB.
        If there has been a change update the field.
        """

        # Convert scraped item to dictionary.
        new_info = new_dict

        # Check for differences between the two dictionaries
        update_dict = dict(new_info.items() - old_dict.items())
        # If DB row and scraped item are different, update the fields that differ.
        if update_dict:
            update_dict['id'] = item['id']

            # Execute update as a transaction to ensure data integrity
            self.db.begin()
            try:
                table.update(
                    update_dict, ['id']
                )
                self.db.commit()

                # If commit is successful publish to the redis server
                self.redis_conn.publish(self.publish_name, update_dict)

            except:
                self.db.rollback()
                raise Exception('Update Transaction Failed: Rolling Back....')

    def insert_transaction(self, item, info, table):
        """
        Ensures new items are sent to the database otherwise a rollback is initiated.

        :param item: The items to be sent to the database
        """

        self.db.begin()
        try:
            table.insert(info)
            self.db.commit()
            self.redis_conn.publish(self.publish_name, info)
        except:
            self.db.rollback()
            raise Exception('Insert Transaction Failed: Rolling Back....')


class InvestingScraperPipeline(DatabaseComponents):

    def __init__(self):
        """
        Initializes the database connection and redis server. Then the table is
        loaded or created.
        """
        DatabaseComponents.__init__(self, 'economic_calendar', 'economic_calendar')

        # Create table if it does not exist otherwise connect to existing table
        if self.table_name in self.db.tables:
            self.table = self.db.load_table(self.table_name)
        else:
            self.table = self.db.create_table(self.table_name, primary_id='id', primary_type=self.db.types.integer)
            self.table.create_column('date', self.db.types.datetime)
            self.table.create_column('currency', self.db.types.string)
            self.table.create_column('importance', self.db.types.integer)
            self.table.create_column('event', self.db.types.string)
            self.table.create_column('actual', self.db.types.float)
            self.table.create_column('forecast', self.db.types.float)
            self.table.create_column('previous', self.db.types.float)
            self.table.create_column('unit', self.db.types.string)

    def process_item(self, item, spider):
        """
        Automatically called after an item has been passed to the pipeline from a spider.
        It's where the pipeline processing begins.

        Here new rows are inserted into the database and changes in rows are updated.
        """

        new_info = dict(
            id=item['id'],
            date=item['date'],
            currency=item['currency'],
            importance=item['importance'],
            event=item['event'],
            actual=item['actual'],
            #actual_unit=item['actual_unit'],
            forecast=item['forecast'],
            #forecast_unit=item['forecast_unit'],
            previous=item['previous'],
            #previous_unit=item['previous_unit'],
            unit=item['unit'],
        )

        # Query the database to see if the item exists in the DB.
        query = "SELECT * FROM " + self.table_name + " WHERE id = " + str(item['id']) + ";"
        df = pd.read_sql_query(query, POSTGRES_DB_URL)

        # If the item does not exist, insert it.
        if len(df.index) == 0:
            self.insert_transaction(item, new_info, self.table)
        # If the item does exist check for changes and update the DB
        else:
            # Convert DB row to dictionary.
            df['date'] = df['date'].dt.strftime("%Y/%m/%d %H:%M:%S")
            old_info = df.to_dict('records')[0]
            self.update_transaction(item, new_info, old_info, self.table)

        return item


class EarningScraperPipeline(DatabaseComponents):

    def __init__(self):
        """
        Initializes the database connection and redis server. Then the table is
        either loaded or created.
        """
        DatabaseComponents.__init__(self, 'earning_calendar', 'earning_calendar')

        if self.table_name in self.db.tables:
            self.table = self.db.load_table(self.table_name)
        else:
            self.table = self.db.create_table(self.table_name, primary_id='id', primary_type=self.db.types.integer)
            self.table.create_column('date', self.db.types.datetime)
            self.table.create_column('country', self.db.types.string)
            self.table.create_column('company', self.db.types.string)
            self.table.create_column('short_code', self.db.types.string)
            self.table.create_column('eps_actual', self.db.types.float)
            self.table.create_column('eps_forecast', self.db.types.float)
            self.table.create_column('rev_actual', self.db.types.bigint)
            self.table.create_column('rev_forecast', self.db.types.bigint)
            self.table.create_column('market_cap', self.db.types.bigint)
            self.table.create_column('market_time', self.db.types.string)

    def process_item(self, item, spider):
        """
        Automatically called after an item has been passed to the pipeline from a spider.
        It's where the pipeline processing begins.

        Here new rows are inserted into the database and changes in rows are updated.
        """

        # Convert scraped item to dictionary.
        new_info = dict(
            id=item['id'],
            date=item['date'],
            country=item['country'],
            company=item['company'],
            short_code=item['short_code'],
            eps_actual=item['eps_actual'],
            eps_forecast=item['eps_forecast'],
            rev_actual=item['rev_actual'],
            rev_forecast=item['rev_forecast'],
            market_cap=item['market_cap'],
            market_time=item['market_time'],
        )

        # Query the database to see if the item exists in the DB.
        query = "SELECT * FROM " + self.table_name + " WHERE id = " + str(item['id']) + ";"
        df = pd.read_sql_query(query, POSTGRES_DB_URL)

        if len(df.index) == 0:
            self.insert_transaction(item, new_info, self.table)
        # If the item does exist check for changes and update the DB
        else:
            # Convert DB row to dictionary.
            df['date'] = df['date'].dt.strftime("%Y/%m/%d %H:%M:%S")
            old_info = df.to_dict('records')[0]
            self.update_transaction(item, new_info, old_info, self.table)

        return item


class NewsScraperPipeline(DatabaseComponents):

    def __init__(self):
        """
        Initializes the database connection and redis server. Then the table is
        loaded or created.
        """
        DatabaseComponents.__init__(self, 'market_news', 'market_news')

        # Create table if it does not exist otherwise connect to existing table
        if self.table_name in self.db.tables:
            self.table = self.db.load_table(self.table_name)
        else:
            self.table = self.db.create_table(self.table_name, primary_id='id', primary_type=self.db.types.integer)
            self.table.create_column('date', self.db.types.datetime)
            self.table.create_column('title', self.db.types.string)
            self.table.create_column('author', self.db.types.string)
            self.table.create_column('text', self.db.types.string)
            self.table.create_column('link', self.db.types.string)

    def process_item(self, item, spider):
        """
        Automatically called after an item has been passed to the pipeline from a spider.
        It's where the pipeline processing begins.

        Here if new rows are found, they are inserted into the database.
        """

        # Convert scraped item to dictionary.
        new_info = dict(
            id=item['id'],
            date=item['date'],
            title=item['title'],
            author=item['author'],
            text=item['text'],
            link=item['link'],

        )
        if not self.table.find_one(id=new_info['id']):  # If PK doesn't exist insert row
            self.db.begin()
            try:
                self.table.insert(new_info)
                self.db.commit()
                self.redis_conn.publish(self.publish_name, new_info)
            except:
                self.db.rollback()
                raise Exception('Insert Transaction Failed: Rolling Back....')

        return item
