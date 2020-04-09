echo
echo VANILLA QUERY
echo 

time echo "SELECT * FROM Asset" | sqlite3 asset.db > /dev/null

echo 
echo IN
echo

time echo "SELECT * FROM Asset WHERE Asset.AssetTicker IN (SELECT AssetTicker FROM AssetValue)" | sqlite3 asset.db > /dev/null

echo
echo NOT IN
echo

time echo "SELECT * FROM Asset WHERE Asset.AssetTicker NOT IN (SELECT AssetTicker FROM AssetValue)" | sqlite3 asset.db > /dev/null
