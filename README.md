# giftlist-api

[![Build Status](https://travis-ci.org/gift-list/giftlist-api.svg?branch=master)](https://travis-ci.org/gift-list/giftlist-api)  [![Coverage Status](https://coveralls.io/repos/gift-list/giftlist-api/badge.svg?branch=master&service=github)](https://coveralls.io/github/gift-list/giftlist-api?branch=master)

Backend api for Gift List creation.

## Documentation
The system is almost entirely composed of an Rest API structure behind a token
authentication system.  The api is also self documenting with a form of swagger.
You can find the documentation here:

<https://fierce-stream-5433.herokuapp.com/docs/>

## Admin
The default django admin is also provided in case there is a need to directly
manipulate objects while development is moving forward.

<https://fierce-stream-5433.herokuapp.com/admin/>

## Contributions
The system can be contributed to via pull requests which will automatically be
built.  New code must not decrease our [code coverage](https://coveralls.io/github/gift-list/giftlist-api)
by more than 5% or drop the total coverage down below 90%.