# -*- coding:utf-8 -*-

import sys
import os
import time
import atexit
import signal

import config
import sms_server
import sms_server_exceptions


class SMSDaemon:
    def __init__(self, pidfile, stdin="/dev/null", stdout="/var/log/sms_server/log", stderr="/var/log/sms_server/err"):
        self._pidfile = pidfile
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr
        self._server = None
        signal.signal(signal.SIGTERM, self._SIGTERM)

    def _daemonize(self):
        sys.stdout.write("Executing daemonize...\n")
        # Делаем первый fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        # Меняем параметры среды
        os.chdir("/")
        os.setsid()
        os.umask(0)
        # Делаем второй fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        # Перенаправляем файловые дескрипторы на файлы из конструктора
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self._stdin, 'r')
        so = file(self._stdout, 'a+')
        se = file(self._stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        # Регистрируем вызов удаления pid-файла при завершении работы и создаем этот файл
        atexit.register(self._delpid)
        pid = str(os.getpid())
        file(self._pidfile, 'w+').write("%s\n" % pid)

    def _delpid(self):
        os.remove(self._pidfile)

    def start(self):
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdin.flush()
        sys.stdout.write("\n" + "SERVER START\n")
        sys.stdout.write("Executing start...\n")
        try:
            pf = file(self._pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self._pidfile)
            sys.exit(1)
        self._daemonize()
        self._launch_server()

    def stop(self):
        try:
            pf = file(self._pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self._pidfile)
            return
        try:
            while 1:
                # TODO: Сделать корректную реакцию на сигнал SIGTERM
                os.kill(pid, signal.SIGKILL)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self._pidfile):
                    os.remove(self._pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def _launch_server(self):
        sys.stdout.write("Executing launch" + "\n")
        raw_conf = config.ConfigReader("/root/SMS_service/config.json")
        conf = config.Config(raw_conf.get_conf_dict())
        self._server = sms_server.SMSServer(conf)
        self._server.start()

    def _SIGTERM(self, signum, stack_frame):
        sys.stdout.write("Executing SIGTERM handler, pid:" + str(os.getpid()) + "\n")
        sys.stdout.write("Received " + signum + "on stackframe " + stack_frame + "\n")
        sys.stdout.write("Stopping server on pid:" + str(os.getpid()))
        try:
            self._server.stop()
        except:
            pass
        sys.stdout.write(" OK\n")
        sys.exit(0)
