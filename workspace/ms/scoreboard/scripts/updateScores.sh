#!/bin/sh

EXPR=/usr/bin/expr
PSQL=/usr/bin/psql

PGUSER=pi
PGDB=msdb
TEAM_TABLE=dbkeeper_team
UPDATE_INTERVAL_S=2

#---
# Main
#---

   # Assumes passwordless authentication is set up properly, e.g. using .pgpass

   moeLaunchDuration_s=0
   moeLaunchScore=1
   moeDockDuration_s=0
   moeDockScore=0
   moeSecureDuration_s=0
   moeSecureScore=0
   moeReturnDuration_s=0
   moeReturnScore=0
   larryLaunchDuration_s=0
   larryLaunchScore=21
   larryDockDuration_s=0
   larryDockScore=0
   larrySecureDuration_s=0
   larrySecureScore=0
   larryReturnDuration_s=0
   larryReturnScore=0
   curlyLaunchDuration_s=0
   curlyLaunchScore=41
   curlyDockDuration_s=0
   curlyDockScore=0
   curlySecureDuration_s=0
   curlySecureScore=0
   curlyReturnDuration_s=0
   curlyReturnScore=0

   while [ 1 ]; do
      moeLaunchDuration_s="`${EXPR} ${moeLaunchDuration_s} + 1`"
      moeLaunchScore="`${EXPR} ${moeLaunchScore} + 2`"
      moeDockDuration_s="`${EXPR} ${moeDockDuration_s} + 1`"
      moeDockScore="`${EXPR} ${moeDockScore} + 1`"
      moeSecureDuration_s="`${EXPR} ${moeSecureDuration_s} + 1`"
      moeSecureScore="`${EXPR} ${moeSecureScore} + 1`"
      moeReturnDuration_s="`${EXPR} ${moeReturnDuration_s} + 1`"
      moeReturnScore="`${EXPR} ${moeReturnScore} + 1`"
      larryLaunchDuration_s="`${EXPR} ${larryLaunchDuration_s} + 1`"
      larryLaunchScore="`${EXPR} ${larryLaunchScore} + 3`"
      larryDockDuration_s="`${EXPR} ${larryDockDuration_s} + 1`"
      larryDockScore="`${EXPR} ${larryDockScore} + 1`"
      larrySecureDuration_s="`${EXPR} ${larrySecureDuration_s} + 1`"
      larrySecureScore="`${EXPR} ${larrySecureScore} + 1`"
      larryReturnDuration_s="`${EXPR} ${larryReturnDuration_s} + 1`"
      larryReturnScore="`${EXPR} ${larryReturnScore} + 1`"
      curlyLaunchDuration_s="`${EXPR} ${curlyLaunchDuration_s} + 1`"
      curlyLaunchScore="`${EXPR} ${curlyLaunchScore} + 4`"
      curlyDockDuration_s="`${EXPR} ${curlyDockDuration_s} + 1`"
      curlyDockScore="`${EXPR} ${curlyDockScore} + 1`"
      curlySecureDuration_s="`${EXPR} ${curlySecureDuration_s} + 1`"
      curlySecureScore="`${EXPR} ${curlySecureScore} + 1`"
      curlyReturnDuration_s="`${EXPR} ${curlyReturnDuration_s} + 1`"
      curlyReturnScore="`${EXPR} ${curlyReturnScore} + 1`"

      if [ ${moeLaunchScore} -gt 100 ]; then
         moeLaunchScore=1
      fi

      if [ ${larryLaunchScore} -gt 100 ]; then
         larryLaunchScore=1
      fi

      if [ ${curlyLaunchScore} -gt 100 ]; then
         curlyLaunchScore=1
      fi

      ${PSQL} -U ${PGUSER} ${PGDB} << END_OF_FILE

         UPDATE ${TEAM_TABLE}
         SET launch_duration_s = ${moeLaunchDuration_s},
             launch_score      = ${moeLaunchScore},
             dock_duration_s   = ${moeDockDuration_s},
             dock_score        = ${moeDockScore},
             secure_duration_s = ${moeSecureDuration_s},
             secure_score      = ${moeSecureScore},
             return_duration_s = ${moeReturnDuration_s},
             return_score      = ${moeReturnScore}
         WHERE name = 'Moe';

         UPDATE ${TEAM_TABLE}
         SET launch_duration_s = ${larryLaunchDuration_s},
             launch_score      = ${larryLaunchScore},
             dock_duration_s   = ${larryDockDuration_s},
             dock_score        = ${larryDockScore},
             secure_duration_s = ${larrySecureDuration_s},
             secure_score      = ${larrySecureScore},
             return_duration_s = ${larryReturnDuration_s},
             return_score      = ${larryReturnScore}
         WHERE name = 'Larry';

         UPDATE ${TEAM_TABLE}
         SET launch_duration_s = ${curlyLaunchDuration_s},
             launch_score      = ${curlyLaunchScore},
             dock_duration_s   = ${curlyDockDuration_s},
             dock_score        = ${curlyDockScore},
             secure_duration_s = ${curlySecureDuration_s},
             secure_score      = ${curlySecureScore},
             return_duration_s = ${curlyReturnDuration_s},
             return_score      = ${curlyReturnScore}
         WHERE name = 'Curly';

         SELECT id, name, launch_duration_s, launch_score, dock_duration_s, dock_score, secure_duration_s, secure_score, return_duration_s, return_score
         FROM ${TEAM_TABLE};

END_OF_FILE

      sleep ${UPDATE_INTERVAL_S}
   done

exit 0
