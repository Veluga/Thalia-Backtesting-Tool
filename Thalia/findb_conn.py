from Finda import fd_manager


class FinDB:
    def __init__(self):
        self.conn = None
        self.server = None

    def register_asset_db(self, server, db_name):

        try:
            db = fd_manager.FdMultiController.fd_connect(db_name, "rwd")
            server.config.update(THALIA_DB_CONN=db)
            self.conn = db
            self.server = server
        except Exception as e:
            print("Fatal: Unable to connect to database " + db_name)
            print(e)
            exit()


findb = FinDB()