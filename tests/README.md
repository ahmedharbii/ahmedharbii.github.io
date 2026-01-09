# Website Tests

This directory contains automated tests for the personal website.

## Running Tests

### Prerequisites
- Python 3.6 or higher

### Run All Tests

From the project root directory:

```bash
python tests/test_website.py
```

## Test Coverage

The test suite includes:

1. **HTML Structure Tests**
   - Verifies all main HTML files exist
   - Checks for proper HTML structure (DOCTYPE, html, head, body tags)
   - Validates closing tags

2. **Meta Tags Tests**
   - Ensures SEO meta tags are present
   - Checks for viewport meta tag (responsive design)
   - Validates Open Graph tags

3. **Asset Tests**
   - Verifies all local images exist
   - Checks CSS file is present and linked
   - Tests for broken internal links

4. **Organization Tests**
   - Validates folder structure
   - Ensures media files are properly organized

5. **Navigation Tests**
   - Checks navigation consistency across pages
   - Validates internal links

6. **Responsive Design Tests**
   - Verifies viewport meta tags
   - Ensures responsive design setup

## CI/CD Integration

Tests run automatically on:
- Every push to main/master branch
- Every pull request

See `.github/workflows/tests.yml` for the GitHub Actions configuration.

## Adding New Tests

To add a new test:

1. Create a new function in `test_website.py` starting with `test_`
2. Add assertion statements
3. Add the function call to `run_all_tests()`
4. Document the test in this README

## Example Output

```
============================================================
Running Website Tests
============================================================

Testing HTML files existence...
  ✓ index.html exists
  ✓ projects.html exists
  ✓ publications.html exists
  ✓ contact.html exists

Testing HTML structure...
  ✓ index.html has valid HTML structure
  ✓ projects.html has valid HTML structure
  ✓ publications.html has valid HTML structure
  ✓ contact.html has valid HTML structure

...

============================================================
✅ All tests passed!
============================================================
```
