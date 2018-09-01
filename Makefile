debug:
	DSB_DEBUG=1 python -m dsb

ui.serve:
	parcel watch -d dsb/static  -o bundle.js --public-url '/static' ui/main.js

package:
	@ echo -e "##### Building UI..."
	parcel build -d dsb/static  -o bundle.js --public-url '/static' ui/main.js
	@ echo -e "\n##### Packaging application..."
	python setup.py sdist
