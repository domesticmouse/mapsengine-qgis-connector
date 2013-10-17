# Makefile for Google Maps Engine Connector for QGIS.
# 
# Copyright 2013 Google Inc.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
PLUGINNAME = GoogleMapsEngineConnector

PY_FILES = __init__.py \
	   plugin/__init__.py \
	   plugin/datamodel/__init__.py

EXTRAS = icon.png \
	 metadata.txt

UI_FILES = plugin/more_dialog_base.py \
	   plugin/signin_dialog_base.py \
	   plugin/wms_dialog_base.py \
	   plugin/search_gme_dialog_base.py \
	   plugin/upload_dialog_base.py

RESOURCE_FILES = resources_rc.py

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%_rc.py : %.qrc
	pyrcc4 -o $*_rc.py  $<

%.py : %.ui
	pyuic4 -o $@ $<

package: compile
	rm -f $(PLUGINNAME).zip
	git archive --format zip --prefix=$(PLUGINNAME)/ -o $(PLUGINNAME).zip $(VERSION) master
	chmod 755 $(PLUGINNAME).zip 

dclean:
	find . -iname "*.pyc" -delete
