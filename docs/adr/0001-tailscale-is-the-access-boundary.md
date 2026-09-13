# Tailscale is the only access control

The app has no login, no user accounts and no in-app authentication. Every
request arrives through `tailscale serve` from a device signed in to the
household's tailnet, which has already authenticated the person and encrypted
the connection. An app password would be a weaker second lock, and installed
iOS PWAs lose their storage often enough that the household would keep getting
logged out.

## Considered Options

- **In-app login**: weaker than the tailnet's identity-provider sign-in, adds
  credential storage and rate limiting, and closes no gap Tailscale leaves open.
- **Per-user accounts**: would need answers to questions the household doesn't
  have, such as whose Draft it is and whose Rejection. A single shared Draft
  lets either partner pick up where the other left off with no extra work.

## Consequences

The boundary holds only while Tailscale is the only way to reach the app:

- The container port is published on loopback only (`127.0.0.1:<port>:<port>`).
  Docker's default binds all interfaces, which would expose the app to anyone on
  the home network, and Docker's iptables rules bypass host firewalls such as
  `ufw`.
- The app is never exposed with Tailscale Funnel, which publishes to the public
  internet.
- Any device on the tailnet can reach the app. If the tailnet grows beyond the
  household, restrict the Pi with an ACL.
- A web page open in the same browser can still send requests to the app.
  Mutating routes must reject cross-site requests. FastAPI refuses a JSON body
  sent with a non-JSON content type, which covers routes that take a body, but a
  route with no body needs its own guard.

Revisit if anyone outside the tailnet needs access, if the app starts storing
data that is costly to lose, or if a feature needs to know which partner acted.
For the last, `tailscale serve` passes identity headers such as
`Tailscale-User-Login`, which should be tried before building accounts.
