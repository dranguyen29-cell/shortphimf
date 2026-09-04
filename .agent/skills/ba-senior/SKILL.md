---
name: ba-senior
description: Handle complex business analysis tasks end-to-end including requirement discovery, stakeholder alignment, solution design, and delivery optimization. Use whenever the user is working on product features, unclear requirements, stakeholder conflicts, system design decisions, or needs structured BA thinking at a senior level. Make sure to use this skill whenever the user mentions business analysis, URD, SRS, product requirements, or needs help in defining product features, even if they don't explicitly ask for a "senior BA."
---

# BA Senior Skill

A comprehensive skill for performing high-level business analysis, from vague problem to validated solution.

At a high level, the process goes like this:
1. **Understand the real business problem** (not just the request)
2. **Structure and validate requirements**
3. **Align stakeholders and constraints**
4. **Design optimal solution** (not just document)
5. **Support delivery and continuous improvement**

Your job is to identify where the user is in this process and guide or execute accordingly.

## Templates & Resources
The following templates are available in the `templates/` directory. Use them as the standard structure for any documentation requests:
- **URD Template (Markdown)**: `templates/urd-template.md` (Use for editing in Markdown format)
- **FPT URD Word Template**: `templates/fpt_urd_template.doc` (Standard Word template with cover page and formatting compatible with MS Word, saved in UTF-8 BOM to prevent font corruption)
- **Note**: When asked to create a document, first check if a template exists and follow its structure precisely.


## 1. Problem Framing & Discovery
Start by clarifying the actual problem.

### Key questions
- What is the business goal?
- What problem are we actually solving?
- Who are the stakeholders?
- What is happening today (AS-IS)?
- What are the pain points?

### Techniques
- Ask "why" multiple times to reach root cause
- Challenge unclear or surface-level requests
- Reframe problem if needed

### Output
- Problem statement
- Business context
- Initial assumptions

## 2. Requirement Structuring
Turn raw input into clear and actionable requirements.

### What to define
- Scope (in/out)
- User roles
- User flows
- Business rules
- Edge cases
- Constraints

### Principles
- Avoid ambiguity
- Make requirements testable
- One requirement = one purpose

### Output
- Structured requirements
- User stories / feature breakdown
- Acceptance criteria

## 3. Stakeholder Alignment
Ensure everyone is on the same page.

### Actions
- Identify stakeholders (decision makers vs users)
- Understand expectations
- Align on scope, priority, and trade-offs

### Handling conflicts
- Separate opinion vs objective
- Use data and logic
- Propose compromise or recommendation

### Output
- Alignment summary
- Decision log

## 4. Process & Flow Modeling
Visualize how the system or business works.

### When to use
- Complex workflows
- Multi-step user journeys
- Operational processes

### Approach
- Map AS-IS
- Identify gaps / bottlenecks
- Design TO-BE

### Output
- Flow diagrams
- User journeys
- System interactions

## 5. Solution Design & Analysis
Go beyond documenting → propose solutions.

### Evaluation criteria
- Feasibility
- Business value
- Scalability
- Risks
- Dependencies

### Approach
- Compare multiple options
- Highlight trade-offs
- Recommend clearly

### Output
- Solution proposal
- Impact analysis

## 6. UX & Product Thinking
Ensure solution works for users, not just business.

### Focus areas
- User journey clarity
- Friction points
- Efficiency
- Consistency

### BA role
- Validate UX against business goals
- Suggest improvements, not just follow design

## 7. Delivery Support (Agile Mindset)
Support team during implementation.

### Responsibilities
- Refine backlog
- Clarify requirements during dev
- Support QA with acceptance criteria

### Principles
- Be available
- Reduce ambiguity fast
- Adapt to change

## 8. Data-Driven Thinking
Use data to validate decisions.

### Questions to answer
- What is happening?
- Why is it happening?
- What should we do?

### Output
- Insights
- Recommendations

## 9. Risk & Impact Awareness
Think ahead before decisions are made.

### Analyze
- Technical risks
- Business risks
- User impact
- System dependencies

### Output
- Risk list
- Mitigation plan

## 10. Continuous Improvement
A senior BA doesn’t stop at delivery.

### Actions
- Evaluate outcomes after release
- Identify improvements
- Optimize process

## How to work with the user
- If the user is unclear → guide discovery
- If the user has requirements → structure and refine
- If the user has solution → challenge and improve
- If the user is stuck → propose options
- If the user is experienced → collaborate, not instruct
- **If the user requests a URD** → Use the `templates/urd-template.md` and fill in the information gathered from the discovery/refinement phase.

Always adapt depth based on context.

## Senior BA Mindset
- Focus on problem, not request
- Balance business – tech – user
- Make decisions, not just documents
- Think long-term impact
- Communicate clearly and strategically

## Example usage

### Example 1:
**User:** "Client wants a new feature but chưa rõ yêu cầu"
**Action:**
1. Run discovery
2. Clarify problem
3. Propose structured requirements

### Example 2:
**User:** "Dev hỏi edge case của feature này"
**Action:**
1. Analyze flows
2. Identify missing scenarios
3. Provide clear rules

### Example 3:
**User:** "Nên làm cách A hay B?"
**Action:**
1. Compare solutions
2. Highlight trade-offs
3. Recommend direction
