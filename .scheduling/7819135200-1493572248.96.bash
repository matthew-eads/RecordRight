
                        #!/bin/bash
                        fname="/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1493572248.96.count"
                        count=`cat $fname`
                        count=$((count-1))
                        if [ $count -lt 1 ]; then
                          # time to die
                          echo "killing self"
                          crontab -l | grep -Fv "/drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1493572248.96.bash" | crontab -
                          rm $fname
                          rm /drives/C/Users/Aristana/DOCUME~1/GitHub/RecordRight/.scheduling/7819135200-1493572248.96.bash
                          exit 0
                        fi
                        echo "not dead yet... decrementing counter"
                        echo $count > $fname
