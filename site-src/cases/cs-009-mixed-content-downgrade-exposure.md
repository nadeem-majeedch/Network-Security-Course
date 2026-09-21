# cs-009 — Mixed-Content and HTTP Downgrade Exposure on a Web App

> **Simulated scenario.** The application, domains, and findings are fictional.

## Difficulty & Domain

- **Difficulty:** Beginner · **Domain:** Network security principles · **CLO:** CLO-1
- **Est. time:** 10 minutes · **Anchor:** L04 (Applied Packet Analysis & Web Protocols)

## Scenario

A university's course-registration web app (`reg.university.example`) is being
migrated to HTTPS. The web team says "we deployed the certificate, we're done."
You are asked to sanity-check the claim before the semester starts. The app
works, students can register — but you have one page source, one HSTS lookup,
and one proxy log.

## Stakeholders

- **Students** — log in with university credentials from café Wi-Fi.
- **Web team** — wants a clean bill of health.
- **Registrar** — accountable for FERPA/GDPR-class data on the app.
- **Attacker (hypothetical)** — anyone on the same open Wi-Fi.

## Network Context

- App served over HTTPS; certificate valid and trusted.
- Registration page loads jQuery from `http://cdn.example-cdn.com` (HTTP).
- Login POST goes to `https://reg.university.example/login`.
- No HSTS header observed on any response.
- The university also serves a legacy redirect: `http://reg.university.example`
  → 302 → `https://...` (the "we redirect everything" claim).

## Available Evidence

1. **Page source (login page):** `<script src="http://cdn.example-cdn.com/jquery.min.js">`
2. **Response headers:** `Server: nginx`, no `Strict-Transport-Security`.
3. **Proxy log (café network simulation):** one student device requested
   `http://reg.university.example/login` first (pre-redirect), then the HTTPS page.
4. **Certificate:** valid, CA-trusted, expires in 60 days.

## Student Task

1. Identify each distinct exposure in this setup and classify its severity for
   a student logging in on open Wi-Fi.
2. For the HTTP-script inclusion: explain what an on-path attacker can and
   cannot do because of it (be precise about TLS boundaries).
3. Give the web team the minimal fix list in priority order, each with the
   reason it matters.

## How to Approach This (Reasoning Scaffold)

- Separate *transport* protection from *content* protection: HTTPS encrypts
  the page, but a page that pulls script over HTTP has a hole in that guarantee.
- The 302 redirect happens **in plaintext** — what does the attacker control
  before the redirect lands?
- HSTS is a *policy memory* feature: think about first-visit exposure.

## CLO Mapping

- **CLO-1** — Web-protocol mechanics → concrete exposure analysis.

## Safety Notes

- Simulated application. Do not probe real university systems; test concepts
  only on lab web servers you control.
