# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, DECIMAL, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'Rules'

    RuleID = Column(Integer, primary_key=True)
    RuleName = Column(String(100), nullable=False, default='DefaultRuleName')
    RuleString = Column(Text, nullable=False)
    RootNodeID = Column(Integer, nullable=True)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    Description = Column(String(255), nullable=True)

    ast_nodes = relationship("ASTNode", back_populates="rule")

class ASTNode(Base):
    __tablename__ = 'ASTNodes'

    NodeID = Column(Integer, primary_key=True)
    NodeType = Column(String(50), nullable=False)
    Value = Column(String(255), nullable=True)
    LeftNodeID = Column(Integer, nullable=True)
    RightNodeID = Column(Integer, nullable=True)
    RuleID = Column(Integer, ForeignKey('Rules.RuleID'), nullable=False)

    rule = relationship("Rule", back_populates="ast_nodes")

class RuleEvaluationHistory(Base):
    __tablename__ = 'RuleEvaluationHistory'

    EvaluationID = Column(Integer, primary_key=True)
    RuleID = Column(Integer, ForeignKey('Rules.RuleID'), nullable=False)
    EvaluationTime = Column(DateTime, default=datetime.utcnow)
    EvaluationResult = Column(Boolean, nullable=False)
    EvaluatedData = Column(Text, nullable=False)

class Attribute(Base):
    __tablename__ = 'Attributes'

    AttributeID = Column(Integer, primary_key=True)
    AttributeName = Column(String(50), nullable=False, unique=True)
    AttributeType = Column(String(20), nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserData(Base):
    __tablename__ = 'UserData'

    UserID = Column(Integer, primary_key=True)
    Age = Column(Integer)
    Department = Column(String(50))
    Salary = Column(DECIMAL(10, 2))
    Experience = Column(Integer)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CombinedRule(Base):
    __tablename__ = 'CombinedRules'

    CombinedRuleID = Column(Integer, primary_key=True)
    CombinedRuleName = Column(String(100), nullable=False)
    CombinedRuleString = Column(Text, nullable=False)
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RuleCombination(Base):
    __tablename__ = 'RuleCombinations'

    RuleCombinationID = Column(Integer, primary_key=True)
    RuleID = Column(Integer, ForeignKey('Rules.RuleID'), nullable=False)
    CombinedRuleID = Column(Integer, ForeignKey('CombinedRules.CombinedRuleID'), nullable=False)