# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openprocurement.api.tests.base import snitch
from openprocurement.api.tests.blanks.document import (
    not_found,
    create_document_in_forbidden_resource_status,
    put_resource_document_invalid,
    create_resource_document_error,
    create_resource_document_json_invalid,
    create_resource_document_json,
    put_resource_document_json
)

from openregistry.lots.ssp.tests.base import (
    LotContentWebTest
)
from openprocurement.api.tests.blanks.json_data import test_ssp_document_data
from openregistry.lots.ssp.constants import DOCUMENT_TYPES
from openregistry.lots.ssp.tests.document_blanks import (
    patch_resource_document,
    model_validation
)

class LotDocumentWithDSResourceTest(LotContentWebTest):
    docservice = True
    document_types = DOCUMENT_TYPES

    test_01_not_found = snitch(not_found)
    test_02_create_document_in_forbidden_resource_status = snitch(create_document_in_forbidden_resource_status)
    test_03_put_resource_document_invalid = snitch(put_resource_document_invalid)
    test_04_patch_resource_document = snitch(patch_resource_document)
    test_05_create_resource_document_error = snitch(create_resource_document_error)
    test_06_create_resource_document_json_invalid = snitch(create_resource_document_json_invalid)
    test_07_create_resource_document_json = snitch(create_resource_document_json)
    test_08_put_resource_document_json = snitch(put_resource_document_json)
    test_09_model_validation = snitch(model_validation)


    # status, in which operations with lot documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active.salable'

    def setUp(self):
        super(LotDocumentWithDSResourceTest, self).setUp()
        self.initial_document_data = deepcopy(test_ssp_document_data)
        self.initial_document_data['url'] = self.generate_docservice_url()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LotDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
