# mend-demo-shop

A small checkout API used to demonstrate [Mend Protocol](https://github.com/Rampop01/Mend-Protocol).

`shop/pricing.py` has a real bug: a coupon that starts with `SAVE` but is not followed by a number, such as `SAVEBIG`, crashes checkout with `ValueError`. The test `test_malformed_save_coupon_is_ignored` describes the intended behaviour and fails on `main`.

## Run it

```bash
pip install -r requirements.txt
python server.py
curl -s -X POST localhost:8000/quote -d '{"items":[{"sku":"tee"}],"coupon":"SAVEBIG"}'
```

With a Mend server watching this repository (`mend connect Rampop01/mend-demo-shop`), the crash is reported, Mend's agents propose and verify a fix, and the approved fix arrives here as a pull request.

## Tests

```bash
python -m unittest discover -s tests -t .
```
