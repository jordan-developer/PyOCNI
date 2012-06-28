# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

# Copyright (C) 2011 Houssem Medhioub - Institut Mines-Telecom
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on Jun 21, 2012

@author: Bilel Msekni
@contact: bilel.msekni@telecom-sudparis.eu
@author: Houssem Medhioub
@contact: houssem.medhioub@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@version: 0.3
@license: LGPL - Lesser General Public License
"""

from webob import Response,Request
from pyocni.registry.entityManager import MultiEntityManager,SingleEntityManager
from pyocni.pyocni_tools.config import return_code
try:
    import simplejson as json
except ImportError:
    import json

import base64

#=======================================================================================================================
#                                           SingleEntityInterface
#=======================================================================================================================
class SingleEntityInterface(object):
    """

        CRUD operation on resources and links

    """
    def __init__(self,req,location):

        self.req = req
        self.location=location
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = SingleEntityManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]


#=======================================================================================================================
#                                           MultiEntityInterface
#=======================================================================================================================
class MultiEntityInterface(object):
    """
    CRUD operation on kinds, mixins and actions
    """
    def __init__(self,req,location,idontknow,idontcare):

        self.req = req
        self.location=location
        self.path_url = self.req.path_url
        self.res = Response()
        self.res.content_type = req.accept
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'
        try:
            self.manager = MultiEntityManager()
        except Exception:
            self.res.body = "An error has occurred, please check log for more details"
            self.res.status_code = return_code["Internal Server Error"]


    def post(self):
        """
        Create a new entity instance or attach resource instance to a mixin database

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]
        jBody = json.loads(self.req.body)
        #add the JSON to database along with other attributes
        self.res.body,self.res.status_code = self.manager.channel_post_multi(user_id,jBody,self.path_url)
        return self.res

    def get(self):
        """
        Gets all entities belonging to a kind or a mixin

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        if self.req.content_type == "text/occi" or self.req.content_type == "text/plain" or self.req.content_type == "text/uri-list":
            # Solution To adopt : Validate HTTP then convert to JSON
            pass
        elif self.req.content_type == "application/json:occi":
            #  Solution To adopt : Validate then convert to application/occi+json
            pass
        elif self.req.content_type == "application/occi+json":
            #Validate the JSON message
            pass
        else:
            self.res.status_code = return_code["Unsupported Media Type"]
            self.res.body = self.req.content_type + " is an unknown request content type"
            return self.res

        #Decode authorization header to get the user_id
        var,user_id = self.req.authorization
        user_id = base64.decodestring(user_id)
        user_id = user_id.split(':')[0]

        if self.req.body == "":
            var,self.res.status_code = self.manager.channel_get_all_entities(self.path_url)
        else:
            jreq = json.loads(self.req.body)
            var,self.res.status_code = self.manager.channel_get_filtered_entities(jreq)

        self.res.body = json.dumps(var)
        return self.res
