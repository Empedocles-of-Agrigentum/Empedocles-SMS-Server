#!/usr/bin/env bash
# Сначала обновим все, что уже установлено
yum -y update
# Затем установим питон
yum -y install python
# Теперь установим библиотеку pyserial для работы с последовательными портами
wget https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz#md5=794506184df83ef2290de0d18803dd11
tar -xzvf pyserial-2.7.tar.gz
cd pyserial-2.7
python setup.py install
# И библиотеку smspdu для транскодирования сообщений в формат PDU
wget https://pypi.python.org/packages/source/s/smspdu/smspdu-1.0.tar.gz#md5=d350d9923c9a943c8e8af6825a41f529
tar -xzvf smspdu-1.0.tar.gz
cd smspdu-1.0
python setup.py install
# И фреймворк для работы с сетью
yum -y install python-twisted
# Создадим папки и файлы для логов и ошибок
mkdir /var/log/sms_server
touch /var/log/sms_server/log
touch /var/log/sms_server/err
