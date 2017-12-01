import dataset
import pandas as pd
import redis


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
        self.redis_conn = redis.StrictRedis()

        # Initialise Database
        self.url = 'postgresql://joseph:password@localhost:5432/postgres'
        self.db = dataset.connect(self.url)
        self.table_name = 'economic_calendar'

        # Create table if it does not exist otherwise connect to existing table
        if self.table_name in self.db.tables:
            self.table = self.db.load_table(self.table_name)
        else:
            self.form_table(self.table_name)

    def process_item(self, item, spider):
        """
        Automatically called after an item has been returned/yielded from a spider.
        It's where the pipeline processing begins.

        Here new rows are inserted into the database changes in rows are updated.
        """

        # Query the database to see if the item exists in the DB.
        query = "SELECT * FROM " + self.table_name + " WHERE id = " + str(item['id']) + ";"
        df = pd.read_sql_query(query, self.url)

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
        # TODO: Fix date problem
        df['date'] = df['date'].dt.strftime("%Y/%m/%d %H:%M:%S")
        old_info = df.to_dict('records')[0]

        # Convert scraped item to dictionary.
        new_info = dict(
                    id=item['id'],
                    date=item['date'],
                    currency=item['currency'],
                    volatility=item['volatility'],
                    event=item['event'],
                    actual=item['actual'],
                    forecast=item['forecast'],
                    previous=item['previous'],
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
                self.redis_conn.publish('economic-calendar', update_dict)

            except:
                self.db.rollback()
                raise Exception('Transaction Failed: Rolling Back....')

    def form_table(self, table_name):
        """
        Create a table, define the columns and data types.

        :param table_name: The name of the table to create
        """
        self.table = self.db.create_table(table_name, primary_id='id', primary_type=self.db.types.integer)
        self.table.create_column('date', self.db.types.datetime)
        self.table.create_column('currency', self.db.types.string)
        self.table.create_column('volatility', self.db.types.string)
        self.table.create_column('event', self.db.types.string)
        self.table.create_column('actual', self.db.types.string)
        self.table.create_column('forecast', self.db.types.string)
        self.table.create_column('previous', self.db.types.string)

    def insert_transaction(self, item):
        """
        Ensures new items are sent to the database otherwise a rollback is initiated.

        :param item: The items to be sent to the database
        """

        info = dict(
            id=item['id'],
            date=item['date'],
            currency=item['currency'],
            volatility=item['volatility'],
            event=item['event'],
            actual=item['actual'],
            forecast=item['forecast'],
            previous=item['previous'],

        )

        self.db.begin()
        try:
            # If rows with matching keys (['id']) exist they will be updated,
            # otherwise a new row is inserted in the table.
            self.table.insert(info)
            self.db.commit()
            self.redis_conn.publish('economic-calendar', info)
        except:
            self.db.rollback()
            raise Exception('Transaction Failed: Rolling Back....')