# Contributing Guidelines

## Code Style

### Python
- Follow PEP 8
- Line length max 100 characters
- Use type hints for functions
- Docstrings for modules and functions

### TypeScript/React
- Use ESLint configuration
- Format with Prettier
- Use functional components
- Props interface for each component

### Git Commits
- Use conventional commits format
- Commit message format: `type(scope): description`
- Types: feat, fix, docs, refactor, perf, test, chore
- Keep commits atomic and focused

Examples:
```
feat(parser): add fuzzy matching for number parsing
fix(voice): handle empty audio input gracefully
docs(api): update endpoint documentation
refactor(services): improve error handling
perf(parser): optimize regex pattern compilation
test(parser): add comprehensive test suite
chore(deps): update dependencies
```

## Development Workflow

1. **Fork and clone:**
   ```bash
   git clone https://github.com/yourusername/credit-tracker.git
   cd credit-tracker
   git switch -c feature/your-feature-name
   ```

2. **Make changes:**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation

3. **Run tests:**
   ```bash
   # Backend tests
   pytest backend/ -v

   # Frontend tests
   npm test

   # Linting
   eslint .
   ruff check backend/
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request:**
   - Describe changes clearly
   - Link related issues
   - Request review from maintainers

## Testing Requirements

- Minimum 80% code coverage
- All new features must have tests
- Run full test suite before submitting PR
- Integration tests for API endpoints

## Documentation Requirements

- Update README for significant features
- Add docstrings to new functions
- Include usage examples for public APIs
- Update ARCHITECTURE.md if design changes

## Performance Considerations

- Profile before optimizing
- Benchmark any critical paths
- Monitor memory usage for models
- Test with production data sizes

## Code Review Process

1. Automated checks (linting, tests)
2. Peer code review
3. Architecture review for major changes
4. Performance testing if needed
5. Security review for API changes

## Reporting Issues

- Use GitHub issues
- Include reproduction steps
- Provide error messages and logs
- Specify environment (OS, Python version, etc.)

## Getting Help

- Check existing documentation
- Search closed issues for similar problems
- Ask on GitHub discussions
- Join community chat (if available)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Acknowledged for significant contributions
