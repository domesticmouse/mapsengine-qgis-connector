Google Maps Engine Connector for QGIS
=====================================

Introduction
------------
Google Maps Engine Connector for QGIS allows your to authenticate with your
Google Account, list maps you have access to and view and interact with them
within QGIS.

[Learn more about Google Maps Engine](
http://www.google.com/enterprise/mapsearth/products/mapsengine.html)

The connector is provided by Google for public use and modification,
but is not covered under the Google Maps Engine
[service level agreement](
http://www.google.com/enterprise/earthmaps/legal/us/gme_sla.html) or
[technical support services](
http://www.google.com/enterprise/earthmaps/legal/us/gme_tssg.html).

Installation
------------
The connector supports QGIS 2.0+ and can be installed via the QGIS plugin
manager.
Plugins -> Manage and Install Plugins -> Google Maps Engine Connector


Overview of the Tools
---------------------
| Tool | Desciption |
| ---- | ---------- |
| ![Sign In](/images/private-16.png) | Sign in or out of your Maps Engine Account. |
| ![Search](/images/search-16.png) | Search for a map from a Google Maps Engine account. Once you select a map and click OK, a bounding box layer is added to the QGIS canvas.* |
| ![Search in Gallery](/images/gallery-16.png) | Search for a Google Maps Engine map in the Google Earth Gallery.* |
| ![WMS](/images/overlay-16.png) | View a layer from the selected map as a WMS overlay in QGIS. ** |
| ![View in GME](/images/maps_engine-16.png) | View the selected map or layer in Google Maps Engine in a new browser tab. ** |
| ![View in Google Maps](/images/maps-16.png) | View the selected map in a Google Maps viewer in a new browser tab. The url includes a short-lived access token allowing access to private maps. ** |
| ![Copy to clipboard](/images/link-16.png) | Copy the link to the WMS service url to clipboard. The url includes a short-lived access token allowing access to private maps. ** |
| ![Upload](/images/upload_item-16.png) | Upload the selected vector or raster layer to Google Maps Engine. *** |
| More | Access *Advanced Settings* and *About dialog*. |

\* *Enabled after a successful login*.

** *Enabled after a successful map search.*

*** *Enabled once a vector layer is selected.*

Updates
-------
QGIS will inform you via a notification in the status bar whenever an update is
available. You can download the new version of the connector by clicking on the
notification. You will also see an update notification when you open the QGIS
plugin manager.

Contributions
-------------

Contributions are welcomed. You can submit a pull request via GitHub.

For your first contribution, you will need to fill out one of the contributor license agreements:

  * If you are the copyright holder, you will need to agree to the <a href="https://developers.google.com/open-source/cla/individual?csw=1">individual contributor license agreement</a>, which can be completed online.
  * If your organization is the copyright holder, the organization will need to agree to the <a href="http://code.google.com/legal/corporate-cla-v1.0.html">corporate contributor license agreement</a>. (If the copyright holder for your code has already completed the agreement in connection with another Google open source project, it does not need to be completed again.)


License
-------
Copyright 2013 Google Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
