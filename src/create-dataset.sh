#!/bin/bash

for MONEY in {100..500..50}
do
  for MISEMIN in {10..100..10}
  do
    MAX=$((MISEMIN + 400))
    for (( MISEMAX=MISEMIN; MISEMAX < MAX; MISEMAX+=50 ))
    do
      for IA in ia-basique ia-hilo ia-hilo-nocount
      do
        echo "${IA} ${MONEY} ${MISEMIN} ${MISEMAX} ${DECK}"
        PYTHONPATH=. python3 main/python/launcher/Launcher.py -j "${IA}" -a "${MONEY}" -p 50 -mn "${MISEMIN}" -mx "${MISEMAX}" -d 5 >> output.txt 2>> error.txt
      done
    done
  done
done

