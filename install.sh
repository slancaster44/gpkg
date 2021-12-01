#!/bin/bash

mkdir /opt/dmi
cp -R ./src/* /opt/dmi

touch /usr/bin/dmi
echo "#!/bin/bash" >> /usr/bin/dmi
echo "/opt/dmi/dmi.py \"\$@\"" >> /usr/bin/dmi
chmod +x /usr/bin/dmi

touch /usr/bin/dmirepo
echo "#!/bin/bash" >> /usr/bin/dmirepo
echo "/opt/dmi/dmirepo.py \"\$@\"" >> /usr/bin/dmirepo
chmod +x /usr/bin/dmirepo