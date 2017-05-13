
    #!/bin/bash
    fname="/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518936.48.count"
    count=`cat $fname`
    count=$((count-1))
    if [ $count -lt 1 ]; then
      # time to die
      echo "killing self"
      crontab -l | grep -Fv "/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518936.48.bash" | crontab -
      /drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/delete_reminder.bash 2
      rm $fname
      rm /drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1494518936.48.bash
      exit 0
    fi
    echo "not dead yet... decrementing counter"
    echo $count > $fname
