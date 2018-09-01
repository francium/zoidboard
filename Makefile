debug:
	DEBUG=1 python -m zoidboard

ui.serve:
	parcel watch -d zoidboard/static  -o bundle.js --public-url '/static' ui/main.js

package:
	@ echo -e "##### Building UI..."
	parcel build -d zoidboard/static  -o bundle.js --public-url '/static' ui/main.js
	@ echo -e "\n##### Packaging application..."
	python setup.py sdist
