mkdir -p db1 db2 db3
mongod --port 27017 --replSet tasksManager --dbpath $(pwd)/db1 &
mongod --port 27018 --replSet tasksManager --dbpath $(pwd)/db2 &
mongod --port 27019 --replSet tasksManager --dbpath $(pwd)/db3 &

sleep 15s # wait for mongodb instances to start

mongosh --eval "rs.initiate({ _id: \"tasksManager\", members: [{_id: 0, host: \"localhost:27017\"}, {_id: 1, host: \"localhost:27018\"}, {_id: 2, host: \"localhost:27019\"}]})" &

echo "Press 'q' to exit"
count=0
while : ; do
read -n 1 k <&1
if [[ $k = q ]] ; then
printf "\nQuitting from the program\n"
break
else
echo "Press 'q' to exit"
fi
done

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
