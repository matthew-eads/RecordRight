
                        #!/bin/bash
                        fname="/home/matt/compsci/RecordRight/.scheduling/4173960290-1493090657.42.count"
                        count=`cat $fname`
                        count=$((count-1))
                        if [ $count -lt 1 ]; then
                          # time to die
                          echo "killing self"
                          crontab -l | grep -Fv "/home/matt/compsci/RecordRight/.scheduling/4173960290-1493090657.42.bash" | crontab -
                          rm $fname
                          rm /home/matt/compsci/RecordRight/.scheduling/4173960290-1493090657.42.bash
                          exit 0
                        fi
                        echo "not dead yet... decrementing counter"
                        echo $count > $fname