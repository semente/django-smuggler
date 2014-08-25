# Django < 1.6 won't discover tests unless they are imported here.
from .test_admin import TestAdminNormalUser, TestAdminSuperUser
from .test_auth import (TestSmugglerViewsAllowsSuperuser,
                        TestSmugglerViewsDeniesNonSuperuser,
                        TestSmugglerViewsRequireAuthentication)
from .test_dump import BasicDumpTestCase
from .test_forms import TestForm
from .test_load import TestInvalidLoad, SimpleLoadTestCase
from .test_urls import TestSmugglerUrls
from .test_utils import TestSaveUploadedFileOnDisk
from .test_views import (TestDumpData,
                         TestDumpHandlesErrorsGracefully,
                         TestDumpViewsGenerateDownloadsWithSaneFilenames,
                         TestLoadDataGet,
                         TestLoadDataPost)

# This list exist to prevent flake8 from complaining.
__tests__ = [
    TestAdminNormalUser,
    TestAdminSuperUser,
    TestSmugglerViewsAllowsSuperuser,
    TestSmugglerViewsDeniesNonSuperuser,
    TestSmugglerViewsRequireAuthentication,
    BasicDumpTestCase,
    TestForm,
    TestInvalidLoad,
    SimpleLoadTestCase,
    TestSmugglerUrls,
    TestSaveUploadedFileOnDisk,
    TestDumpData,
    TestDumpHandlesErrorsGracefully,
    TestDumpViewsGenerateDownloadsWithSaneFilenames,
    TestLoadDataGet,
    TestLoadDataPost
]
