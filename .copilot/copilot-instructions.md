# Copilot Instructions - OpenOA Web Application

## 📋 Project Context

This is a web application that exposes the OpenOA Python library (wind plant operational assessment) as a web service. The goal is to create a professional demo for an interview.

**Repository Structure:**
- `backend/` - FastAPI Python backend
- `frontend/` - React TypeScript frontend  
- `openoa/` - The existing OpenOA library (DO NOT MODIFY)

---

## 🎯 General Guidelines

### Code Quality Standards
1. **Write clean, readable code** - Prioritize clarity over cleverness
2. **Follow language conventions** - PEP 8 for Python, ESLint/Prettier for TypeScript
3. **Add meaningful comments** - Explain "why", not "what"
4. **Use type hints/types** - Python type hints, TypeScript strict mode
5. **Keep functions small** - Single responsibility principle
6. **Handle errors gracefully** - Never expose raw errors to users

### File Organization
1. **One component/module per file** - Easy to find and maintain
2. **Group by feature, not type** - Keep related code together
3. **Use index files for exports** - Clean import statements
4. **Consistent naming conventions** - See language-specific guidelines

### Git Practices
1. **Small, focused commits** - One logical change per commit
2. **Meaningful commit messages** - Describe what and why
3. **Don't commit secrets** - Use .env files, add to .gitignore

---

## 🔒 Security Best Practices

### Never Do
- Hardcode API keys, passwords, or secrets
- Trust user input without validation
- Expose detailed error messages to clients
- Commit .env files or credentials
- Disable CORS in production

### Always Do
- Validate and sanitize all inputs
- Use environment variables for configuration
- Implement proper CORS settings
- Add rate limiting for public APIs
- Log security-relevant events

---

## 🧪 Testing Guidelines

### Backend Testing
- Use pytest for all tests
- Test API endpoints with TestClient
- Mock external dependencies (OpenOA calls)
- Aim for >80% coverage on critical paths
- Test error handling paths

### Frontend Testing
- Use Vitest for unit tests
- Use React Testing Library for components
- Test user interactions, not implementation
- Mock API calls with MSW or similar

---

## 📝 Documentation Standards

### Code Documentation
- Docstrings for all public functions (Python)
- JSDoc comments for exported functions (TypeScript)
- README.md in each major directory
- Keep docs updated with code changes

### API Documentation
- FastAPI auto-generates OpenAPI docs
- Add descriptions to all endpoints
- Include request/response examples
- Document error responses

---

## 🚀 Deployment Considerations

### Render.com Specific
- Use `render.yaml` for infrastructure-as-code
- Set environment variables in Render dashboard
- Use health check endpoints
- Consider cold start times (free tier)

### Environment Parity
- Development should mirror production
- Use Docker for consistent environments
- Same versions of Python/Node
- Test with production-like data

---

## 🔗 Integration with OpenOA

### Importing OpenOA
```python
# Backend should import from the installed openoa package
from openoa.analysis import MonteCarloAEP
from openoa import PlantData
```

### Best Practices
1. **Don't modify OpenOA source** - Use it as a dependency
2. **Create service wrappers** - Isolate OpenOA logic in services/
3. **Handle OpenOA exceptions** - Wrap in try/catch, return user-friendly errors
4. **Use sample data for demos** - Don't require user uploads initially

---

## 📁 Reference Documentation

For language-specific guidelines, see:
- [Backend Instructions](./backend.md) - FastAPI/Python specifics
- [Frontend Instructions](./frontend.md) - React/TypeScript specifics
