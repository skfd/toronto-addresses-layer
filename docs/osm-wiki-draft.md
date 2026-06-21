# OSM wiki update — draft

Draft text for registering the Toronto address layers and tools on the
OpenStreetMap wiki. Edit as needed, then paste into the wiki.

## Where each piece goes

- **Draft 1** — new top-level section on the [Toronto wiki page](https://wiki.openstreetmap.org/wiki/Toronto),
  placed right after the existing **"City of Toronto Open Data"** section.
  Log in with an OSM wiki account → *Edit source* → paste.
- **Draft 2** — one catalogue row on
  [WikiProject Canada/Open data](https://wiki.openstreetmap.org/wiki/WikiProject_Canada/Open_data),
  adapted to the page's existing table/list style.

> The change-tracker description is inferred from the README/landing-page
> cross-links (its repo is not in this workspace). Verify before publishing.

---

## Draft 1 — section for the Toronto wiki page (wikitext)

```wikitext
== Address points reference layers and tools ==

The City of Toronto publishes its [https://open.toronto.ca/dataset/address-points-municipal-toronto-one-address-repository/ Address Points (Municipal)] dataset (525,000+ points, already in WGS84) under the [https://open.toronto.ca/open-data-licence/ Open Government Licence – Toronto], which is [[Toronto#City of Toronto Open Data|compatible with OpenStreetMap]].

Two community tools turn this dataset into map-editor reference overlays and a change tracker. '''These are reference layers, not a bulk import''' — verify against survey or imagery before adding anything to OSM.

=== Toronto Address Points reference layer ===

Pre-rendered map tiles of every municipal address point, refreshed daily, for use as a reference overlay while mapping in iD and JOSM.

* Landing page (with copy-paste instructions): https://skfd.github.io/toronto-addresses-layer/
* Source code: https://github.com/skfd/toronto-addresses-layer

Two layers are produced:

{| class="wikitable"
! Layer !! Format !! Best in !! Notes
|-
| Vector || MVT (.pbf) || iD || Interactive — click a point to read its <code>addr</code>, <code>housenumber</code>, <code>street</code>, <code>class</code> tags. Rendered natively through zoom 19.
|-
| Raster || PNG || JOSM || House numbers drawn as readable text over the tiles. A backdrop for tracing. Zooms 16–19 (editors overzoom past z19).
|}

'''Add to iD''' — Map Data panel (<kbd>U</kbd>) → Custom Map Data, paste:
 https://skfd.github.io/toronto-addresses-layer/tiles/vector/{z}/{x}/{y}.pbf
or the raster background:
 https://skfd.github.io/toronto-addresses-layer/tiles/raster/{z}/{x}/{y}.png

'''Add to JOSM''' — Preferences → Imagery → +TMS, paste (note JOSM uses <code>{zoom}</code>, not <code>{z}</code>):
 tms[16,18]:https://skfd.github.io/toronto-addresses-layer/tiles/raster/{zoom}/{x}/{y}.png

=== Toronto address change tracker ===

A sibling project that tracks how the City's address dataset changes over time, to help find new, moved, or removed addresses that may need attention in OSM.

* Site: https://skfd.github.io/toronto-addresses-import/
* Source code: https://github.com/skfd/toronto-addresses-import

=== See also ===

A submission to the [https://github.com/osmlab/editor-layer-index Editor Layer Index] is planned so the raster layer appears directly in the iD and JOSM imagery pickers for the Toronto area.
```

---

## Draft 2 — row for WikiProject Canada/Open data

```wikitext
* '''Toronto Address Points''' — 525,000+ municipal address points, [https://open.toronto.ca/open-data-licence/ OGL – Toronto]. Available as daily-refreshed iD/JOSM reference tile layers (vector + raster) at https://skfd.github.io/toronto-addresses-layer/ and as a change tracker at https://skfd.github.io/toronto-addresses-import/ . Reference only, not a bulk import.
```

---

## Notes before publishing

- OSM wiki accounts may be separate from the osm.org login — create/confirm a
  wiki account first.
- The Toronto page links internally with `[[Toronto#...]]`; double-check the
  exact heading text on the live page and adjust the anchor.
- Optional next step: open an Editor Layer Index PR for the raster layer
  (TMS, zooms 16–19, Toronto bounding polygon, OGL – Toronto licence) so it
  appears automatically in the iD/JOSM imagery pickers.
