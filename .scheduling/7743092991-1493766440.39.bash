
		#!/bin/bash
		fname="/Users/akarukappadath/Documents/School/DevRegions/RecordRight/.scheduling/7743092991-1493766440.39.count"
		count=`cat $fname`
		count=$((count-1))
		if [ $count -lt 1 ]; then
		# time to die
		echo "killing self"
		crontab -l | grep -Fv "/Users/akarukappadath/Documents/School/DevRegions/RecordRight/.scheduling/7743092991-1493766440.39.bash" | crontab -
		rm $fname
		rm /Users/akarukappadath/Documents/School/DevRegions/RecordRight/.scheduling/7743092991-1493766440.39.bash
		exit 0
		fi
		echo "not dead yet... decrementing counter"
		echo $count > $fname
