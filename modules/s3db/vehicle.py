# -*- coding: utf-8 -*-

""" Sahana Eden Vehicle Model

    @copyright: 2009-2017 (c) Sahana Software Foundation
    @license: MIT

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
"""

__all__ = ("S3VehicleModel",)

from gluon import *
from gluon.storage import Storage

from ..s3 import *

# =============================================================================
class S3VehicleModel(S3Model):
    """
        Vehicle Management Functionality

        http://eden.sahanafoundation.org/wiki/BluePrint/Vehicle
    """

    names = ("vehicle_vehicle",
             "vehicle_vehicle_id",
             )

    def model(self):

        T = current.T
        db = current.db

        configure = self.configure
        crud_strings = current.response.s3.crud_strings
        define_table = self.define_table
        float_represent = IS_FLOAT_AMOUNT.represent
        int_represent = IS_INT_AMOUNT.represent

        # ---------------------------------------------------------------------
        # Vehicles
        #   a type of Asset
        #
        tablename = "vehicle_vehicle"
        define_table(tablename,
                     self.asset_asset_id(),
                     Field("name",
                           comment = T("e.g. License Plate"),
                           label = T("ID"),
                           ),
                     Field("gps",
                           label = T("GPS ID"),
                           ),
                     Field("mileage", "integer",
                           label = T("Current Mileage"),
                           represent = lambda v: int_represent(v),
                           ),
                     Field("service_mileage", "integer",
                           comment = T("Mileage"),
                           label = T("Service Due"),
                           represent = lambda v: int_represent(v),
                           ),
                     s3_date("service_date",
                             label = T("Service Due"),
                             ),
                     s3_date("insurance_date",
                             label = T("Insurance Renewal Due"),
                             ),
                     s3_comments(),
                     *s3_meta_fields())

        # CRUD strings
        crud_strings[tablename] = Storage(
            label_create = T("Add Vehicle Details"),
            title_display = T("Vehicle Details"),
            title_list = T("Vehicles"),
            title_update = T("Edit Vehicle Details"),
            label_list_button = T("List Vehicle Details"),
            label_delete_button = T("Delete Vehicle Details"),
            msg_record_created = T("Vehicle Details added"),
            msg_record_modified = T("Vehicle Details updated"),
            msg_record_deleted = T("Vehicle Details deleted"),
            msg_list_empty = T("No Vehicle Details currently defined"))

        represent = S3Represent(lookup=tablename)
        vehicle_id = S3ReusableField("vehicle_id", "reference %s" % tablename,
                                     label = T("Vehicle"),
                                     ondelete = "RESTRICT",
                                     represent = represent,
                                     requires = IS_EMPTY_OR(
                                                    IS_ONE_OF(db,
                                                              "vehicle_vehicle.id",
                                                              represent,
                                                              )),
                                     )

        configure(tablename,
                  context = {"location": "asset_id$location_id"
                             },
                  )

        # ---------------------------------------------------------------------
        # Pass names back to global scope (s3.*)
        #
        return dict(vehicle_vehicle_id = vehicle_id,
                    )

    # -------------------------------------------------------------------------
    @staticmethod
    def defaults():
        """ Return safe defaults for names in case the model is disabled """

        dummy = S3ReusableField("dummy_id", "integer",
                                readable = False,
                                writable = False)

        return dict(vehicle_vehicle_id = lambda **attr: dummy("vehicle_id"),
                    )

# END =========================================================================
