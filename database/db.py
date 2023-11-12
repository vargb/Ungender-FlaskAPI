import flaskServer.config.config as Config

dbUrl = (
    "postgresql://"
    + Config.conf.postgres.user
    + ":"
    + Config.conf.postgres.password
    + "@"
    + Config.conf.postgres.host
    + ":"
    + Config.conf.postgres.sqlport
    + "/"
    + Config.conf.postgres.dbname
)
