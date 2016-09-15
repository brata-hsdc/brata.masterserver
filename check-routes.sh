#!/bin/sh
# We need to figure out how to ensure the pi stops changing the route order so this is not needed.
while true; do
   # wait for route to get screwed up
   while ip route show | head -1 | grep -q 172; do echo "[`date`] Routes good!"; sleep 60; done

   echo "[`date`] Fixing routes!!!"
   sudo ip route restore < /home/pi/goodroutes
   sleep 30
done
