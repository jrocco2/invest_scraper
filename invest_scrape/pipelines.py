import dataset
import pandas as pd
import redis
from invest_scrape.settings import POSTGRES_DB_URL, POSTGRES_TABLE_NAME, REDIS_HOST, REDIS_PORT, REDIS_PUBLISH_NAME

class InvestingScraperPipeline(object):
    """
    Pipeline to retrieve scraped fields from InvestingScraperItem instance and
    send them to a Postgres database and redis server.
    """

    def __init__(self):
        """
        Initializes the database connection and redis server. Then the table is
        loaded or created.
        """

        # Initialise Redis
        self.redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

        # Initialise Database
        self.db = dataset.connect(POSTGRES_DB_URL)

        # Create table if it does not exist otherwise connect to existing table
        if POSTGRES_TABLE_NAME in self.db.tables:
            self.table = self.db.load_table(POSTGRES_TABLE_NAME)
        else:
            self.form_table(POSTGRES_TABLE_NAME)

    def process_item(self, item, spider):
        """
        Automatically called after an item has been returned/yielded from a spider.
        It's where the pipeline processing begins.

        Here new rows are inserted into the database changes in rows are updated.
        """

        # Query the database to see if the item exists in the DB.
        query = "SELECT * FROM " + POSTGRES_TABLE_NAME + " WHERE id = " + str(item['id']) + ";"
        df = pd.read_sql_query(query, POSTGRES_DB_URL)

        # If the item does not exist, insert it.
        if len(df.index) == 0:
            self.insert_transaction(item)
        # If the item does exist check for changes and update the DB
        else:
            self.update_transaction(item, df)

        return item

    def update_transaction(self, item, df):
        """
        Check for differences between the item scraped and the row in the DB.
        If there has been a change update the field.
        """

        # Convert DB row to dictionary.
        df['date'] = df['date'].dt.strftime("%Y/%m/%d %H:%M:%S")
        old_info = df.to_dict('records')[0]

        # Convert scraped item to dictionary.
        new_info = dict(
                    id=item['id'],
                    date=item['date'],
                    currency=item['currency'],
                    importance=item['importance'],
                    event=item['event'],
                    actual=item['actual'],
                    actual_unit=item['actual_unit'],
                    forecast=item['forecast'],
                    forecast_unit=item['forecast_unit'],
                    previous=item['previous'],
                    previous_unit=item['previous_unit'],
                    )

        # Check for differences between the two dictionaries
        update_dict = dict(new_info.items() - old_info.items())

        # If DB row and scraped item are different, update the fields that differ.
        if update_dict:
            update_dict['id'] = item['id']

            # Execute update as a transaction to ensure data integrity
            self.db.begin()
            try:
                self.table.update(
                    update_dict, ['id']
                )
                self.db.commit()

                # If commit is successful publish to the redis server
                self.redis_conn.publish(REDIS_PUBLISH_NAME, update_dict)

            except:
                self.db.rollback()
                raise Exception('Update Transaction Failed: Rolling Back....')

    def form_table(self, table_name):
        """
        Create a table, define the columns and data types.

        :param table_name: The name of the table to create
        """
        self.table = self.db.create_table(table_name, primary_id='id', primary_type=self.db.types.integer)
        self.table.create_column('date', self.db.types.datetime)
        self.table.create_column('currency', self.db.types.string)
        self.table.create_column('importance', self.db.types.integer)
        self.table.create_column('event', self.db.types.string)
        self.table.create_column('actual', self.db.types.string)
        self.table.create_column('actual_unit', self.db.types.string)
        self.table.create_column('forecast', self.db.types.string)
        self.table.create_column('forecast_unit', self.db.types.string)
        self.table.create_column('previous', self.db.types.string)
        self.table.create_column('previous_unit', self.db.types.string)

    def insert_transaction(self, item):
        """
        Ensures new items are sent to the database otherwise a rollback is initiated.

        :param item: The items to be sent to the database
        """

        info = dict(
                    id=item['id'],
                    date=item['date'],
                    currency=item['currency'],
                    importance=item['importance'],
                    event=item['event'],
                    actual=item['actual'],
                    actual_unit=item['actual_unit'],
                    forecast=item['forecast'],
                    forecast_unit=item['forecast_unit'],
                    previous=item['previous'],
                    previous_unit=item['previous_unit'],
                    )

        self.db.begin()
        try:
            # If rows with matching keys (['id']) exist they will be updated,
            # otherwise a new row is inserted in the table.
            self.table.insert(info)
            self.db.commit()
            self.redis_conn.publish(REDIS_PUBLISH_NAME, info)
        except:
            self.db.rollback()
            raise Exception('Insert Transaction Failed: Rolling Back....')
