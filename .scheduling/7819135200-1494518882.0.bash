
    #!/bin/bash
    fname="/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518882.0.count"
    count=`cat $fname`
    count=$((count-1))
    if [ $count -lt 1 ]; then
      # time to die
      echo "killing self"
      crontab -l | grep -Fv "/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518882.0.bash" | crontab -
      /drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/delete_reminder.bash 1
      rm $fname
      rm /drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518882.0.bash
      exit 0
    fi
    echo "not dead yet... decrementing counter"
    echo $count > $fname
