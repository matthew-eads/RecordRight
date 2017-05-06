
    #!/bin/bash
    fname="/home/matt/compsci/RecordRight/.scheduling/notanumber-1494089277.67.count"
    count=`cat $fname`
    count=$((count-1))
    if [ $count -lt 1 ]; then
      # time to die
      echo "killing self"
      crontab -l | grep -Fv "/home/matt/compsci/RecordRight/.scheduling/notanumber-1494089277.67.bash" | crontab -
      /home/matt/compsci/RecordRight/delete_reminder.bash 8
      rm $fname
      rm /home/matt/compsci/RecordRight/.scheduling/notanumber-1494089277.67.bash
      exit 0
    fi
    echo "not dead yet... decrementing counter"
    echo $count > $fname
