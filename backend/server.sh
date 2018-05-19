#!/usr/bin/env bash

PYTHON_ACTIVATE_FILE="bin/activate"
UWSGI_CMD="bin/uwsgi"
UWSGI_CONF_FILE="conf/uwsgi.yaml"
UWSGI_PID_FILE="tmp/uwsgi.pid"
LOG_DIR="log"
TMP_DIR="tmp"
LOG_FILE="$LOG_DIR/server.log"

function execute {
    $1 >> ${LOG_FILE} 2>&1 # Execute the command
    if [ $? -ne 0 ]; then # Check the return code of command
        echo "Error in executing command: $1. Please check log file log/server.log"
        exit 1
    fi
}

function start {
    if [ ! -f ${PYTHON_ACTIVATE_FILE} ]; then
        echo "$PYTHON_ACTIVATE_FILE not found"
        exit 1
    fi

    if [ -f ${UWSGI_PID_FILE} ]; then
        echo "Server is already running. pid file: $UWSGI_PID_FILE"
        exit 1
    fi

    if [ ! -d ${LOG_DIR} ]; then
        mkdir $LOG_DIR # Execute the command
        if [ $? -ne 0 ]; then # Check the return code of command
            echo "Error in creating log file."
            exit 1
        fi
    fi

    if [ ! -d ${TMP_DIR} ]; then
        mkdir $TMP_DIR # Execute the command
        if [ $? -ne 0 ]; then # Check the return code of command
            echo "Error in creating log file."
            exit 1
        fi
    fi

    if [ ! -x ${UWSGI_CMD} ]; then
        echo "$UWSGI_CMD not found or not executable"
        exit 1
    fi

    if [ ! -f ${UWSGI_CONF_FILE} ]; then
        echo "$UWSGI_CONF_FILE not found"
        exit 1
    fi

    echo "Starting server"
    execute "source $PYTHON_ACTIVATE_FILE"
    echo "Python executable: `which python`" > ${LOG_FILE}
    execute "$UWSGI_CMD $UWSGI_CONF_FILE"
    sleep 2

    kill -0 `cat ${UWSGI_PID_FILE}`  > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error in starting server. Please check log file log/server.log"
        exit 1
    fi

    echo "Server started"
}

function stop {
    if [ ! -f ${PYTHON_ACTIVATE_FILE} ]; then
        echo "$PYTHON_ACTIVATE_FILE not found"
        exit 1
    fi

    if [ ! -f ${UWSGI_PID_FILE} ]; then
        echo "Server is not running. pid file not found: $UWSGI_PID_FILE"
        if [ "$1" == "--ignore" ]; then
            return
        else
            exit 1
        fi
    fi

    if [ ! -d ${LOG_DIR} ]; then
        echo "Log folder not found: $LOG_DIR"
        exit 1
    fi

    if [ ! -x ${UWSGI_CMD} ]; then
        echo "$UWSGI_CMD not found or not executable"
        exit 1
    fi

    echo "Stopping server"
    execute "source $PYTHON_ACTIVATE_FILE"
    echo "Python executable: `which python`" > ${LOG_FILE}
    execute "$UWSGI_CMD --stop $UWSGI_PID_FILE"
    sleep 5

    kill -0 `cat ${UWSGI_PID_FILE}` > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Error in stopping server. Please check log file log/server.log"
        exit 1
    fi

    execute "rm $UWSGI_PID_FILE"
    echo "Server stopped"
}

function cmd_help {
    echo "Commands start|stop|restart"
}

########################################################################

if [ $# -lt 1 ];then
    cmd_help
    exit 1
fi

case $1 in
    "start")
        start
        ;;

    "stop")
        stop
        ;;

    "restart")
        stop --ignore
        start
        ;;
    *)
        echo "Unable to recognize command: $1"
        cmd_help
        ;;
esac