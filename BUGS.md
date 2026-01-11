# Project Bug & Issue Report

Generated: 2026-01-11

## Summary ✅
This document lists the issues I found by scanning the repository (templates, models, views). Issues are grouped by priority and include short remediation steps so you can decide what to fix first.

---

## High priority (can cause runtime errors) ⚠️

- **Template iteration over variations may fail**
  - Files: `templates/store/product_detail.html`, `templates/store/product_detail2.html`
  - Problem: Template uses `{% for i in single_product.variation_set.colors %}` and `.sizes`. These rely on methods not guaranteed on the related manager and can raise template errors.
  - Risk: 500 server error (TemplateSyntaxError / AttributeError).
  - Recommendation: Query Variation objects in the `product_detail` view and pass `color_variations` and `size_variations` to the template; iterate those instead.

- **Image fields accessed without guard**
  - Files: `templates/store/product_detail.html`, `templates/store/store.html`
  - Problem: Code like `{{ single_product.images.url }}` will raise if `images` is missing.
  - Risk: AttributeError -> 500 error.
  - Recommendation: In templates, check `{% if product.images %}` before using `.url` or provide a default placeholder image.

- **Broad and improper exception handling in view**
  - File: `store/views.py` (function: `product_detail`)
  - Problem: `except Exception as msg: raise msg` - re-raising the exception object can lose stack and broad except hides specific failures.
  - Risk: Harder debugging and unexpected handling of unrelated exceptions.
  - Recommendation: Use specific exception handling (e.g., `Product.DoesNotExist`) or remove the try/except and allow Django to handle/raise naturally.

---

## Medium priority (accessibility / UX) 🔧

- **Missing `alt` attributes on images**
  - Files: `templates/store/product_detail.html`, `templates/store/store.html`
  - Problem: `<img>` tags missing `alt` attributes.
  - Risk: Accessibility violations and poor SEO.
  - Recommendation: Add descriptive `alt` text (e.g., `alt="{{ product.product_name }}"`).

- **Form labels not associated with controls**
  - Files: `templates/store/product_detail.html`, `templates/store/store.html`
  - Problem: `<label>` elements without `for` attributes or corresponding `id` on inputs.
  - Risk: Accessibility (screen reader) issues.
  - Recommendation: Add `id` to inputs and `for` to labels.

- **Table headers missing `scope` or `id`**
  - File: `templates/orders/order_complete.html`
  - Problem: `<th>` elements lacking `scope` attributes.
  - Risk: Accessibility and table semantics.
  - Recommendation: Add `scope="col"` (or `row`) to table header cells.

- **Commented out code and empty inline styles**
  - Files: various templates (e.g., `templates/base.html`, `templates/store/store.html`)
  - Problem: commented blocks and `style=""`/empty ruleset warnings.
  - Recommendation: Clean up stale comments and remove empty inline styles.

---

## Low priority (maintainability / best practice) ✨

- **Commented code in models/views**
  - Files: `store/models.py`, `store/views.py`
  - Recommendation: Remove or document code being kept for a purpose.

- **Use of `IntegerField` for price**
  - File: `store/models.py`
  - Note: `price = models.IntegerField()` may be fine if storing cents, otherwise `DecimalField` is recommended for currency.

- **Minor template HTML semantics**
  - Files: several. e.g. star rating labels may not be visually bound to the inputs.
  - Recommendation: verify styles and label associations so that the rating input is accessible and usable.

---

## Suggested next steps (pick one) ✅

1. Run the Django test suite and static checks (non-modifying) and report failing tests.  
2. Create GitHub issues (one per item) so you can triage and assign fixes.  
3. Prepare a branch/PR with non-invasive fixes (template guards, view changes, accessibility improvements).  

Tell me which option you prefer and I will proceed.

---

## Notes
- I only scanned for common issues (templates, models, views). If you want, I can run deeper checks (security linting, static analyzers, test execution, or add unit tests).

---

*End of report*
