# Enrollment playback-link test correction — proposal for human review

**Proposal approved by avinash2196; recorded 2026-10-27T04:26:57Z.** The user approved this exact narrow test-correction proposal in the main conversation. This authorizes the normal documentation review sequence, not this pending Plan revision, an Implementation Plan, test/source application or milestone completion. The user-retained working changes remain intact;013 remains blocked and is not ready for approval.

The first actual host-context disposable GREEN dry run reached all97 cases and reported **95 passed,2 failed in422.15s**:38 feature passes and all57 preserved regressions. The only failures were test_guidance_formats_playback_admission_and_originals at line251 and test_multistream_metadata_playback_and_conditioning at line513: returned-link playback received404 instead of200. This is planning evidence, not milestone execution or a passing GREEN result.

The approved contract defines public paths under configured public_base_url plus /api/v1; a valid returned playback URL must reach that endpoint. The unchanged test fixture creates HTTPX clients with base_url ending/api/v1. Both tests strip the returned URL to path/query using urlsplit and pass that path to the client. HTTPX appends even a leading-slash path to the base path. An actual build_request check produced:

```text
base_url=http://127.0.0.1:1234/api/v1
input=/api/v1/artifacts/example/content -> http://127.0.0.1:1234/api/v1/api/v1/artifacts/example/content
input=/artifacts/example/content -> http://127.0.0.1:1234/api/v1/artifacts/example/content
```

Returning/artifacts/... solely to satisfy that client is not a valid repair: an origin-relative URL resolves outside the actual/api/v1 route in a browser. Adding a production alias or inventing service-relative URL semantics would change the approved behavior. Earlier RED runs stopped at missing imports and did not exercise these link-following lines.

Recommend correcting only the test transport: resolve the returned URL with standard URL joining against the fixture origin/base, assert that the result stays on that local origin, then give the absolute URL to the existing HTTPX client. Preserve both authenticated original-byte/format/playback assertions, the unauthenticated401 assertion, independent selected-stream comparison, and every other existing assertion. Exactly three request sites change across two test bodies; no production behavior or public schema changes. No fixture model, limit or security bypass is added.

## Exact proposed test diff — not applied

```diff
--- a/tests/test_voice_enrollment.py
+++ b/tests/test_voice_enrollment.py
@@ -5,7 +5,7 @@
 import hashlib
 import importlib
 import json
-from urllib.parse import urlsplit
+from urllib.parse import urljoin, urlsplit
 
 import numpy as np
 import pytest
@@ -190,6 +190,14 @@
     return result
 
 
+def returned_link_url(system, value):
+    base = str(system["media"].base_url)
+    resolved = urljoin(base, value)
+    expected, actual = urlsplit(base), urlsplit(resolved)
+    assert (actual.scheme, actual.netloc) == (expected.scheme, expected.netloc), "Playback stays on the fixture origin"
+    return resolved
+
+
 def create_profile(system, samples, **changes):
     body = {"name": "मेरा निजी स्वर", "language": "hi",
             "consent_id": system["consent_record"]["consent_id"],
@@ -246,13 +254,13 @@
                                    headers=headers(s["token"]))
         assert result.status_code == 200, result.text
         link = result.json()
-        parts = urlsplit(link["url"])
-        content = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
+        playback_url = returned_link_url(s, link["url"])
+        content = s["media"].get(playback_url, headers=headers(s["token"]))
         assert content.status_code == 200 and content.content == data
         assert "inline" in content.headers["content-disposition"]
         assert content.headers["content-type"].split(";")[0] == {
             "wav": "audio/wav", "mp3": "audio/mpeg", "m4a": "audio/mp4"}[fmt]
-        error(s["media"].get(parts.path + "?" + parts.query), 401, "UNAUTHENTICATED")
+        error(s["media"].get(playback_url), 401, "UNAUTHENTICATED")
         error(s["media"].get("/artifacts/" + sample["artifact_id"] + "/download-url?format=wav",
                                headers=headers(s["token"])), 400, "UNSUPPORTED_FORMAT")
     for data, fmt, code in [(b"", "wav", "INVALID_AUDIO"), (b"not audio", "wav", "INVALID_AUDIO"),
@@ -508,8 +516,8 @@
     response = s["media"].get("/artifacts/" + sample["artifact_id"] + "/preview-url",
                                  headers=headers(s["token"]))
     assert response.status_code == 200, response.text
-    parts = urlsplit(response.json()["url"])
-    playback = s["media"].get(parts.path + "?" + parts.query, headers=headers(s["token"]))
+    playback_url = returned_link_url(s, response.json()["url"])
+    playback = s["media"].get(playback_url, headers=headers(s["token"]))
     assert playback.status_code == 200 and playback.content == data
     assert independent_decode(playback.content)["stream_index"] == captured["stream_index"]
```

## Review and execution sequence

If accepted, record this narrow test-wiring correction through the normal approved Plan revision and a separate OTHER Implementation Plan before editing tests. Keep completed012 history/evidence intact; do not recast a failing GREEN as success or silently change its tests. Then revise013 against that approved interface, run the complete97-case disposable verification twice, preserve all57 regressions and user-retained source, and present013 for its own review. The current proposal does not authorize that later code/test execution. No second97 run was performed against the known contradictory seam.

Authority: current requirements FR-010/011/012/013 and Q11/Q12; approved API-Contract.md shared URL scope, Artifact Link/access and common rules; Plan milestone14 Pending; approved010/012 tests and interfaces; actual installed HTTPX joining behavior;013 planning diagnostics. No new product decision, requirement number or public URL format is introduced.
