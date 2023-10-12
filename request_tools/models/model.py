#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
from typing import Text, Dict, Optional, List
from pydantic import BaseModel



class IMages(BaseModel):
    cmdb: Optional[str]  = None
    eventti: Optional[str] = None
    gway: Optional[str] = None
    httpd: Optional[str] = None
    inet_client: Optional[str] = None
    inet_client_java: Optional[str] = None
    inet_ngparser: Optional[str] = None
    inet_platform: Optional[str] = None
    inet_workflow: Optional[str] = None
    json_adaptor: Optional[str] = None
    logsystem: Optional[str] = None
    netc: Optional[str] = None
    netd: Optional[str] = None
    nginx: Optional[str] = None
    pipeline: Optional[str] = None
    policyinsight: Optional[str] = None
    trigger: Optional[str] = None




