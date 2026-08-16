# Local Target

The public demo is convenient for smoke checks but is shared infrastructure. Mutation, load, and
failure-injection testing should use an owned deployment.

The helper script installs the open-source Restful Booker Platform at the commit used during this
framework build:

```powershell
.\scripts\target.ps1 setup
.\scripts\target.ps1 start
```

The upstream build currently requires JDK 26, Maven 3.9.14, Node 24.14.1, npm 11.11.0, and Docker.
The upstream build script compiles the services and starts its Docker Compose project. When it is
healthy, point this framework at the URL printed by the upstream script (the upstream README uses
`http://localhost:3003`):

```powershell
$env:TEST_BASE_URL = "http://localhost:3003"
pytest -m smoke --browser chromium
pytest -m mutation --run-mutation --browser chromium
```

Inspect or stop it with:

```powershell
.\scripts\target.ps1 status
.\scripts\target.ps1 stop
```

The source is cloned under `.target/`, which is ignored. To evaluate a newer upstream revision,
pass `-Ref <commit>` to `setup`, validate the full suite, and update the default only in a reviewed
change. The target remains a separate GPL-3.0 project; none of its source is redistributed here.
