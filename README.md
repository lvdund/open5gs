1. First, you need to build and install:
```bash
cd open5gs
rm -rf build
meson build --prefix=$(pwd)/install -Dc_args=-O2
ninja -C build
ninja -C build install
```
2. Then run the 5G Core (all NFs) using:
run individual NFs like:
```bash
ln -s /home/vd/github/open5gs/install/lib64/libprom.so /home/vd/github/open5gs/install/lib/


./install/bin/open5gs-nrfd
./install/bin/open5gs-amfd
./install/bin/open5gs-smfd
./install/bin/open5gs-upfd
./install/bin/open5gs-ausfd
./install/bin/open5gs-udmd
./install/bin/open5gs-pcfd
./install/bin/open5gs-nssfd
./install/bin/open5gs-bsfd
./install/bin/open5gs-udrd
```
3. Web:
- Username : admin
- Password : 1423

```bash
cd webui
npm ci
HOSTNAME=0.0.0.0 npm run dev
```

4. Add ue:
```bash
python3 webui/web.py ue --op -n 10
python3 webui/web.py ue --opc -n 10

python3 webui/web.py ue -c
```
