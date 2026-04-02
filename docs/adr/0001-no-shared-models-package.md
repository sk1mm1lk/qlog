# ADR 0001: No Shared Models Package Between Client and Server

## Status

Accepted

## Context

The client and server both deal with the same shape of data, and one way to ensure that the data is valid being sent from the client was to create a `yaki-shared` package that both have to import.

## Decision

The client should remain thin and dumb at the moment, and the effort it would take create that is not worth the hassle at this point in time. Will be reconsidered later down the line.
