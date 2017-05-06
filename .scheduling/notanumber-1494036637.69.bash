
        #!/bin/bash
        fname="/home/matt/compsci/RecordRight/.scheduling/notanumber-1494036637.69.count"
        count=`cat $fname`
        count=$((count-1))
        if [ $count -lt 1 ]; then
        # time to die
        echo "killing self"
        crontab -l | grep -Fv "/home/matt/compsci/RecordRight/.scheduling/notanumber-1494036637.69.bash" | crontab -
        rm $fname
        rm /home/matt/compsci/RecordRight/.scheduling/notanumber-1494036637.69.bash
        exit 0
        fi
        echo "not dead yet... decrementing counter"
        echo $count > $fname
