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



