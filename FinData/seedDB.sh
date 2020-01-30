#Populate database with some easy to outdated biz memes for testing
#If you are reading this in a different branch to db-adaptor remove it
#as i've probably already written better testing code,
#with more appropriate names

echo "INSERT INTO Asset VALUES
  ('RCK','Rock','CRYPTO'),
  ('BRY', 'Berry', 'CRYPTO'),
  ('GLU', 'Glue', 'PETROLIUM DERIVATIVE'),
  ('GAS','Gasoline','PETROLIUM DERIVATIVE'),
  ('<3','NULLASSET','CRYPTO')
  ;" | sqlite3 finData.db


echo "INSERT INTO AssetClass VALUES
    ('CRYPTO'),
    ('PETROLIUM DERIVATIVE'),
    ('NULLCLASS')
    ;" | sqlite3 finData.db

echo "INSERT INTO AssetValue VALUES
    ('RCK','2020-1-1','1.1','1.1','1.1','1.1',0),
    ('RCK','2020-1-2','1.2','1.2','1.2','1.2',1),
    ('RCK','2020-1-3','1.3','1.3','1.3','1.3',0),
    ('BRY','2020-1-2','3.1','3.1','3.1','3.1',0),
    ('BRY','2020-1-3','2.3','2.3','2.3','2.3',0),
    ('BRY','2020-1-4','1.4','1.4','1.4','1.4',0),
    ('GLU','2020-1-2','4.2','4.2','4.2','4.2',0),
    ('GLU','2020-1-3','5.3','5.3','5.3','5.3',0)
  ;" | sqlite3 finData.db



