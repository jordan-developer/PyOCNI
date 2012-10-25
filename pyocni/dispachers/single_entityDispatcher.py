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
from pyocni.adapters.i_ResponseAdapter import ResponseAdapter
from pyocni.adapters.i_RequestAdapter import RequestAdapter
from pyocni.junglers.single_entityJungler import SingleEntityJungler
from pyocni.pyocni_tools.config import return_code
try:
    import simplejson as json
except ImportError:
    import json


#=======================================================================================================================
#                                           SingleEntityInterface
#=======================================================================================================================
class SingleEntityDispatcher(object):
    """

        dispachers operation on resources and links

    """
    def __init__(self,req,location,idontknow=None,idontcare=None):

        self.req = req

        self.location=location
        self.idontknow = idontknow
        self.idontcare = idontcare

        self.path_url = self.req.path_url
        self.triggered_action = None

        self.res = Response()
        self.res.content_type = str(req.accept)
        self.res.server = 'ocni-server/1.1 (linux) OCNI/1.1'

        self.req_adapter = RequestAdapter()
        self.res_adapter = ResponseAdapter()
        self.jungler = SingleEntityJungler()



    def put(self):

        """
        Create a new entity instance with a customized URL or perform a full update of the resource
        """
        #Step[1]: Detect the body type (HTTP ,JSON:OCCI or OCCI+JSON)

        jBody = self.req_adapter.convert_request_entity_content(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:
            #Step[2]: Treat the request
            var,self.res.status_code = self.jungler.channel_put_single_resource(jBody,self.path_url)

            #Step[3]: Adapt the response to the required accept-type

            if self.res.status_code == return_code['OK, and location returned']:

                self.res = self.res_adapter.convert_response_entity_location_content(var,self.res)
            else:
                self.res.content_type = "text/html"
                self.res.body = var

        return self.res

    def get(self):

        """
        Retrieve the representation of a resource
        """
        #add the JSON to database along with other attributes

        var,self.res.status_code = self.jungler.channel_get_single_resource(self.path_url)

        if self.res.status_code == return_code['OK']:

            self.res = self.res_adapter.convert_response_entity_content(self.res,var)

        else:
            self.res.content_type = "text/html"
            self.res.body = var

        return self.res

    def post(self):
        """
        Perform a partial update of a resource
        """
        if self.req.params.has_key('action'):
            self.triggered_action = self.req.params['action']

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)

        jBody = self.req_adapter.convert_request_entity_content_v2(self.req)

        if jBody is None:

            self.res.status_code = return_code['Not Acceptable']
            self.res.body = self.req.content_type + " is an unknown request content type"

        else:

            #add the JSON to database along with other attributes
            if self.triggered_action is None:

                var,self.res.status_code = self.jungler.channel_post_single_resource(jBody,self.path_url)

                if self.res.status_code == return_code['OK, and location returned']:

                    self.res = self.res_adapter.convert_response_entity_location_content(var,self.res)
                else:
                    self.res.content_type = "text/html"
                    self.res.body = var

            else:

                self.res.body,self.res.status_code = self.jungler.channel_triggered_action_single(jBody,self.path_url,self.triggered_action)

        return self.res


    def delete(self):
        """
        Delete a resource instance

        """

        #Detect the body type (HTTP ,OCCI:JSON or OCCI+JSON)


        #add the JSON to database along with other attributes
        self.res.body,self.res.status_code = self.jungler.channel_delete_single_resource(self.path_url)

        return self.res

