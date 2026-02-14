import pandas as pd
import numpy as np

class SuccessScoringAgent:
    """
    Success Scoring Agent that takes a user_id as input and outputs:
    - Sustained Usage Score
    - Workflow Depth Score
    - Serious Engagement Score
    - Tier Classification
    - Risk Level
    - Personalized Recommendations
    """
    
    def __init__(self, user_segments_df):
        """Initialize agent with user_segments data"""
        self.user_data = user_segments_df.set_index('user_id')
        self.score_columns = ['sustained_usage_score', 'workflow_depth_score', 'serious_usage_score']
        
    def get_user_scores(self, user_id):
        """Get success scores for a specific user"""
        if user_id not in self.user_data.index:
            return None
        
        user = self.user_data.loc[user_id]
        
        # Extract core metrics
        scores = {
            'user_id': user_id,
            'sustained_usage_score': round(user['sustained_usage_score'], 2),
            'workflow_depth_score': round(user['workflow_depth_score'], 2),
            'serious_usage_score': round(user['serious_usage_score'], 2),
            'composite_success_score': round(user['composite_success_score'], 2),
            'tier_classification': user['success_tier'],
            'days_active': int(user['days_active']),
            'total_events': int(user['total_events']),
            'execution_events': int(user['execution_event_count']),
            'unique_event_types': int(user['unique_event_types']),
            'total_credits_used': round(user['total_credits_used'], 2),
            'tool_invocations': int(user['tool_invocation_count'])
        }
        
        # Calculate risk level
        scores['risk_level'] = self._calculate_risk_level(user)
        
        # Generate personalized recommendations
        scores['recommendations'] = self._generate_recommendations(user)
        
        return scores
    
    def _calculate_risk_level(self, user):
        """Calculate risk level based on engagement patterns"""
        tier = user['success_tier']
        days_active = user['days_active']
        composite_score = user['composite_success_score']
        execution_rate = user['execution_event_rate']
        
        # Risk scoring logic
        if tier in ['Power Users', 'Active Users']:
            if days_active >= 7 and execution_rate > 0.3:
                return 'Low Risk'
            elif days_active >= 3:
                return 'Medium Risk'
            else:
                return 'High Risk - May Churn'
        
        elif tier == 'Regular Users':
            if days_active >= 3 and execution_rate > 0.1:
                return 'Medium Risk'
            else:
                return 'High Risk - Needs Activation'
        
        else:  # Casual and Trial Users
            if days_active == 1:
                return 'Critical Risk - Early Stage'
            elif composite_score < 2:
                return 'Critical Risk - Low Engagement'
            else:
                return 'High Risk - Needs Onboarding'
    
    def _generate_recommendations(self, user):
        """Generate personalized recommendations based on user profile"""
        recommendations = []
        tier = user['success_tier']
        
        # Sustained usage recommendations
        if user['sustained_usage_score'] < 2:
            recommendations.append("🎯 Increase Sustained Usage: Encourage daily logins and consistent workflow building")
            if user['days_active'] < 3:
                recommendations.append("   → Set up reminder emails to return to the platform")
        
        # Workflow depth recommendations
        if user['workflow_depth_score'] < 10:
            recommendations.append("🔧 Develop Workflow Depth: Introduce advanced features like Fleet, multiple block types, and complex DAGs")
            if user['execution_event_count'] == 0:
                recommendations.append("   → Critical: User hasn't executed any code blocks yet - provide execution tutorial")
            elif user['unique_event_types'] < 10:
                recommendations.append("   → Show feature discovery prompts for unused block types")
        
        # Serious engagement recommendations
        if user['serious_usage_score'] < 5:
            recommendations.append("💪 Boost Serious Engagement: Promote credit usage through AI features and advanced compute")
            if user['total_credits_used'] == 0:
                recommendations.append("   → Offer free credits trial to demonstrate value of premium features")
            if user['tool_invocation_count'] < 10:
                recommendations.append("   → Highlight AI assistant capabilities and tool usage examples")
        
        # Tier-specific recommendations
        if tier == 'Trial Users':
            recommendations.append("🚀 Trial User Focus: Provide strong onboarding and quick-win tutorials")
            recommendations.append("   → Send welcome email series with use case templates")
        
        elif tier == 'Casual Users':
            recommendations.append("📈 Casual User Activation: Show ROI through case studies and template galleries")
            recommendations.append("   → Enable social proof (community showcase, user success stories)")
        
        elif tier == 'Regular Users':
            recommendations.append("⚡ Regular User Growth: Introduce collaboration features and advanced workflows")
            if user['unique_canvases'] < 3:
                recommendations.append("   → Encourage multi-project usage with project templates")
        
        elif tier == 'Active Users':
            recommendations.append("🎖️ Active User Retention: Offer premium features preview and team plans")
            recommendations.append("   → Provide beta access to new features")
        
        elif tier == 'Power Users':
            recommendations.append("👑 Power User Excellence: Maintain engagement with exclusive content and direct support")
            recommendations.append("   → Invite to advisory board or user research programs")
        
        # Credit-specific recommendations
        if user['total_credits_used'] > 0 and user['total_credits_used'] < 1:
            recommendations.append("💳 Credit Conversion Opportunity: User tested credits - offer upgrade package")
        
        return recommendations
    
    def get_batch_scores(self, user_ids):
        """Get scores for multiple users"""
        results = []
        for uid in user_ids:
            score = self.get_user_scores(uid)
            if score:
                results.append(score)
        return pd.DataFrame(results)
    
    def summarize_user(self, user_id):
        """Print a comprehensive summary for a user"""
        scores = self.get_user_scores(user_id)
        
        if not scores:
            print(f"❌ User ID '{user_id}' not found in dataset")
            return None
        
        print("=" * 100)
        print(f"🎯 SUCCESS SCORING AGENT - USER ANALYSIS")
        print("=" * 100)
        print(f"\n👤 User ID: {scores['user_id']}")
        print(f"\n📊 SUCCESS SCORES:")
        print(f"  • Sustained Usage Score:    {scores['sustained_usage_score']:8.2f}  (consistency & return behavior)")
        print(f"  • Workflow Depth Score:     {scores['workflow_depth_score']:8.2f}  (feature usage & complexity)")
        print(f"  • Serious Engagement Score: {scores['serious_usage_score']:8.2f}  (credits & tool invocations)")
        print(f"  • Composite Success Score:  {scores['composite_success_score']:8.2f}  (weighted combination)")
        
        print(f"\n🏆 CLASSIFICATION:")
        print(f"  • Tier:       {scores['tier_classification']}")
        print(f"  • Risk Level: {scores['risk_level']}")
        
        print(f"\n📈 KEY METRICS:")
        print(f"  • Days Active:          {scores['days_active']:5d}")
        print(f"  • Total Events:         {scores['total_events']:5d}")
        print(f"  • Execution Events:     {scores['execution_events']:5d}")
        print(f"  • Unique Event Types:   {scores['unique_event_types']:5d}")
        print(f"  • Credits Used:         {scores['total_credits_used']:8.2f}")
        print(f"  • Tool Invocations:     {scores['tool_invocations']:5d}")
        
        print(f"\n💡 PERSONALIZED RECOMMENDATIONS:")
        for i, rec in enumerate(scores['recommendations'], 1):
            print(f"  {rec}")
        
        print("\n" + "=" * 100)
        
        return scores


# Initialize the Success Scoring Agent
scoring_agent = SuccessScoringAgent(user_segments)

print("✅ Success Scoring Agent initialized!")
print(f"📊 Loaded {len(user_segments)} users")
print("\n" + "=" * 100)
print("🎯 EXAMPLE USAGE:")
print("=" * 100)

# Demonstrate with a sample user from each tier
print("\n📌 Analyzing sample users from different tiers...\n")

# Get sample users from each tier
tier_samples = {}
for tier in ['Power Users', 'Active Users', 'Regular Users', 'Casual Users', 'Trial Users']:
    tier_users = user_segments[user_segments['success_tier'] == tier]
    if len(tier_users) > 0:
        # Pick user with median composite score for that tier
        median_idx = len(tier_users) // 2
        tier_samples[tier] = tier_users.sort_values('composite_success_score').iloc[median_idx]['user_id']

# Analyze one example user (Active User)
if 'Active Users' in tier_samples:
    example_user_id = tier_samples['Active Users']
    example_scores = scoring_agent.summarize_user(example_user_id)
    
print("\n" + "=" * 100)
print("📚 AGENT INTERFACE:")
print("=" * 100)
print("""
The Success Scoring Agent provides these methods:

1. scoring_agent.get_user_scores(user_id)
   Returns a dictionary with all scores, tier, risk, and recommendations

2. scoring_agent.summarize_user(user_id)
   Prints a formatted report and returns scores dictionary

3. scoring_agent.get_batch_scores([user_id1, user_id2, ...])
   Returns a DataFrame with scores for multiple users

Example:
  scores = scoring_agent.get_user_scores('USER_ID_HERE')
  print(scores['composite_success_score'])
  print(scores['tier_classification'])
  print(scores['recommendations'])
""")