# /bin/bash

echo "starting monitoring MQTT"

echo "Counter AvgRuntime(sec) MsgTimeMin(ms) MsgTimeMax(ms) MsgTimeMean(ms) MsgTimeStd(ms) AvgBandwidth(msg/sec) TimeStamp" >> mosquittoLoadResults.txt
echo "Counter AvgRuntime(sec) MsgTimeMin(ms) MsgTimeMax(ms) MsgTimeMean(ms) MsgTimeStd(ms) AvgBandwidth(msg/sec) TimeStamp" 


CONTADOR=0

while true; do
	./mqtt-benchmark --broker tcp://192.168.0.199:1883 --count 100 --size 1500 --clients 100 --qos 2 --format text > test.txt
	TIMESTAMP=$(date +%D-%H:%M:%S)
	MIN=$(tail -n 10 test.txt | grep min | awk {print'$5'})
	MAX=$(tail -n 10 test.txt | grep max | awk {print'$5'})
	MEAN=$(tail -n 10 test.txt | grep "mean mean" | awk {print'$6'})
	STD=$(tail -n 10 test.txt | grep "std" | awk {print'$6'})
	AVGRUNTIME=$(tail -n 10 test.txt | grep "Average Runtime" | awk {print'$4'})
	AVGBANDWIDTH=$(tail -n 10 test.txt | grep "Average Bandwidth" | awk {print'$4'})
	echo $CONTADOR $AVGRUNTIME $MIN $MAX $MEAN $STD $AVGBANDWIDTH $TIMESTAMP >> mosquittoLoadResults.txt
	echo $CONTADOR $AVGRUNTIME $MIN $MAX $MEAN $STD $AVGBANDWIDTH $TIMESTAMP 
	rm test.txt
        #if [ $CONTADOR>30 ]
        #then
	echo "starting AVM evaluation"
        python3 avm/codePythonAVM.py $MEAN
        #sleep 30
        #fi
	sleep 30
	CONTADOR=$(echo $CONTADOR+1 | bc)
done
