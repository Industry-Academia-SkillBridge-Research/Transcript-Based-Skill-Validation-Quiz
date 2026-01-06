import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Spinner } from '../components/ui/Spinner';
import { ErrorAlert } from '../components/ui/ErrorAlert';
import { getSkillExplanation } from '../api/api';
import { ChevronLeft, ChevronDown, Info, TrendingUp, BookOpen, Award } from 'lucide-react';

export function SkillExplainPage() {
  const { studentId, skillName } = useParams();
  const navigate = useNavigate();
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadExplanation();
  }, [studentId, skillName]);

  const loadExplanation = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getSkillExplanation(studentId, skillName, 'parent');
      setExplanation(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getLevelColor = (level) => {
    const colors = {
      'Beginner': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'Intermediate': 'bg-blue-100 text-blue-800 border-blue-200',
      'Advanced': 'bg-green-100 text-green-800 border-green-200'
    };
    return colors[level] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 50) return 'text-blue-600';
    return 'text-yellow-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <Spinner size="large" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 p-6">
        <div className="max-w-4xl mx-auto">
          <ErrorAlert message={error} />
          <Button onClick={() => navigate(`/students/${studentId}/skills`)} className="mt-4">
            <ChevronLeft className="w-4 h-4 mr-2" />
            Back to Skills
          </Button>
        </div>
      </div>
    );
  }

  if (!explanation) return null;

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex items-start justify-between">
          <div>
            <Button 
              variant="ghost" 
              onClick={() => navigate(`/students/${studentId}/skills`)}
              className="mb-4"
            >
              <ChevronLeft className="w-4 h-4 mr-2" />
              Back to Skills
            </Button>
            <div className="flex items-center gap-3">
              <Info className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-3xl font-bold text-slate-900">{explanation.skill_name}</h1>
                <p className="text-slate-600 mt-1">Detailed Score Breakdown</p>
              </div>
            </div>
          </div>
          <div className="text-right">
            <div className={`text-5xl font-bold ${getScoreColor(explanation.score)}`}>
              {explanation.score}
            </div>
            <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium border mt-2 ${getLevelColor(explanation.level)}`}>
              {explanation.level}
            </span>
          </div>
        </div>

        <Card className="border-blue-200 shadow-lg">
          <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50">
            <h2 className="text-2xl font-bold flex items-center gap-2 text-blue-900">
              <TrendingUp className="w-6 h-6 text-blue-600" />
              How This Score Was Calculated
            </h2>
            <p className="text-sm text-slate-600 mt-1">
              Your score is based on your academic performance in related courses
            </p>
          </CardHeader>
          <CardContent className="space-y-6 pt-6">
            {/* Main Calculation Formula */}
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-xl shadow-md">
              <div className="text-sm font-semibold mb-4 opacity-90 flex items-center gap-2">
                <div className="w-6 h-6 bg-white/20 rounded-full flex items-center justify-center text-xs">📐</div>
                STEP-BY-STEP SCORE CALCULATION
              </div>
              
              {/* Step 1: Show Formula */}
              <div className="bg-white/10 rounded-lg p-4 mb-4">
                <div className="text-xs opacity-80 mb-2">Step 1: The Formula</div>
                <div className="font-mono text-lg font-bold">
                  Score = (Total Contribution ÷ Total Weight) × 100
                </div>
              </div>

              {/* Step 2: Substitute Values */}
              <div className="bg-white/10 rounded-lg p-4 mb-4">
                <div className="text-xs opacity-80 mb-2">Step 2: Substitute Your Values</div>
                <div className="font-mono text-lg font-bold">
                  Score = ({explanation.calculation.total_contribution} ÷ {explanation.calculation.total_weight}) × 100
                </div>
              </div>

              {/* Step 3: Calculate Division */}
              <div className="bg-white/10 rounded-lg p-4 mb-4">
                <div className="text-xs opacity-80 mb-2">Step 3: Divide Total Contribution by Total Weight</div>
                <div className="font-mono text-lg font-bold">
                  Score = {(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)} × 100
                </div>
                <div className="text-xs opacity-70 mt-1">
                  ({explanation.calculation.total_contribution} ÷ {explanation.calculation.total_weight} = {(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)})
                </div>
              </div>

              {/* Step 4: Final Result */}
              <div className="bg-white/20 rounded-lg p-4 border-2 border-white/40">
                <div className="text-xs opacity-80 mb-2">Step 4: Multiply by 100 to Get Percentage</div>
                <div className="font-mono text-xl font-bold">
                  Score = {explanation.score}%
                </div>
                <div className="text-xs opacity-70 mt-1">
                  ({(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)} × 100 = {explanation.score}%)
                </div>
              </div>

              {/* Visual Representation */}
              <div className="mt-6 pt-4 border-t border-white/30">
                <div className="text-xs opacity-80 mb-3 text-center">Visual Breakdown</div>
                <div className="grid grid-cols-5 gap-2 items-center text-center">
                  <div className="bg-white/20 rounded-lg p-3">
                    <div className="text-2xl font-bold">{explanation.calculation.total_contribution}</div>
                    <div className="text-xs opacity-90 mt-1">Contribution</div>
                  </div>
                  <div className="text-3xl font-bold">÷</div>
                  <div className="bg-white/20 rounded-lg p-3">
                    <div className="text-2xl font-bold">{explanation.calculation.total_weight}</div>
                    <div className="text-xs opacity-90 mt-1">Weight</div>
                  </div>
                  <div className="text-3xl font-bold">×</div>
                  <div className="bg-white/20 rounded-lg p-3">
                    <div className="text-2xl font-bold">100</div>
                    <div className="text-xs opacity-90 mt-1">Percentage</div>
                  </div>
                </div>
                <div className="text-center mt-4">
                  <div className="inline-block bg-yellow-400 text-blue-900 px-6 py-3 rounded-lg">
                    <div className="text-xs font-semibold">YOUR FINAL SCORE</div>
                    <div className="text-4xl font-bold">{explanation.score}%</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Detailed Scoring Methodology */}
            <div className="space-y-6">
              <h3 className="font-bold text-xl text-slate-900 flex items-center gap-2 border-b-2 border-blue-200 pb-2">
                <Info className="w-6 h-6 text-blue-600" />
                Understanding the Scoring Method
              </h3>

              {/* Step 1: Grade to Contribution */}
              <div className="border-2 border-blue-200 rounded-xl p-5 bg-gradient-to-br from-blue-50 to-white">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">1</div>
                  <h4 className="font-bold text-lg text-slate-900">Grade → Contribution Points</h4>
                </div>
                <p className="text-sm text-slate-700 mb-4">
                  Your letter grade in each course is converted to contribution points. Higher grades earn more points:
                </p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  <div className="bg-green-100 border border-green-300 rounded p-2 text-center">
                    <div className="font-bold text-green-800">A+</div>
                    <div className="text-xs text-green-700">4.0 points</div>
                  </div>
                  <div className="bg-green-100 border border-green-300 rounded p-2 text-center">
                    <div className="font-bold text-green-800">A</div>
                    <div className="text-xs text-green-700">4.0 points</div>
                  </div>
                  <div className="bg-lime-100 border border-lime-300 rounded p-2 text-center">
                    <div className="font-bold text-lime-800">A-</div>
                    <div className="text-xs text-lime-700">3.7 points</div>
                  </div>
                  <div className="bg-lime-100 border border-lime-300 rounded p-2 text-center">
                    <div className="font-bold text-lime-800">B+</div>
                    <div className="text-xs text-lime-700">3.3 points</div>
                  </div>
                  <div className="bg-yellow-100 border border-yellow-300 rounded p-2 text-center">
                    <div className="font-bold text-yellow-800">B</div>
                    <div className="text-xs text-yellow-700">3.0 points</div>
                  </div>
                  <div className="bg-yellow-100 border border-yellow-300 rounded p-2 text-center">
                    <div className="font-bold text-yellow-800">B-</div>
                    <div className="text-xs text-yellow-700">2.7 points</div>
                  </div>
                  <div className="bg-orange-100 border border-orange-300 rounded p-2 text-center">
                    <div className="font-bold text-orange-800">C+</div>
                    <div className="text-xs text-orange-700">2.3 points</div>
                  </div>
                  <div className="bg-orange-100 border border-orange-300 rounded p-2 text-center">
                    <div className="font-bold text-orange-800">C</div>
                    <div className="text-xs text-orange-700">2.0 points</div>
                  </div>
                </div>
              </div>

              {/* Step 2: Weight Calculation */}
              <div className="border-2 border-purple-200 rounded-xl p-5 bg-gradient-to-br from-purple-50 to-white">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold">2</div>
                  <h4 className="font-bold text-lg text-slate-900">Calculate Weight for Each Course</h4>
                </div>
                <p className="text-sm text-slate-700 mb-4">
                  Weight determines how important each course is. It's calculated using three factors:
                </p>
                <div className="space-y-3">
                  <div className="bg-white border-l-4 border-purple-400 p-3 rounded">
                    <div className="font-semibold text-purple-900 text-sm mb-1">📚 Credits (Higher = More Important)</div>
                    <p className="text-xs text-slate-600">A 4-credit course has more weight than a 2-credit course</p>
                  </div>
                  <div className="bg-white border-l-4 border-purple-400 p-3 rounded">
                    <div className="font-semibold text-purple-900 text-sm mb-1">📅 Recency (Recent = More Relevant)</div>
                    <p className="text-xs text-slate-600">Recent courses (e.g., 2024) get higher weight than older ones (e.g., 2020)</p>
                  </div>
                  <div className="bg-white border-l-4 border-purple-400 p-3 rounded">
                    <div className="font-semibold text-purple-900 text-sm mb-1">🎯 Map Weight (Skill Relevance)</div>
                    <p className="text-xs text-slate-600">How strongly the course content relates to this specific skill (0.0 to 1.0)</p>
                  </div>
                </div>
                <div className="mt-4 bg-purple-100 p-3 rounded-lg">
                  <div className="font-mono text-sm text-purple-900">
                    Weight = Credits × Recency × Map_Weight
                  </div>
                </div>
              </div>

              {/* Step 3: Final Score */}
              <div className="border-2 border-indigo-200 rounded-xl p-5 bg-gradient-to-br from-indigo-50 to-white">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-bold">3</div>
                  <h4 className="font-bold text-lg text-slate-900">Calculate Final Score</h4>
                </div>
                <p className="text-sm text-slate-700 mb-4">
                  Multiply each course's grade points by its weight, then divide by total weight:
                </p>
                <div className="bg-indigo-100 p-4 rounded-lg space-y-2">
                  <div className="font-mono text-sm text-indigo-900">
                    For each course: Weighted_Contribution = Grade_Points × Weight
                  </div>
                  <div className="font-mono text-sm text-indigo-900">
                    Total_Contribution = Sum of all Weighted_Contributions
                  </div>
                  <div className="font-mono text-sm text-indigo-900">
                    Total_Weight = Sum of all Weights
                  </div>
                  <div className="mt-3 pt-3 border-t-2 border-indigo-300">
                    <div className="font-mono text-base font-bold text-indigo-900">
                      Final Score = (Total_Contribution ÷ Total_Weight) × 100
                    </div>
                  </div>
                </div>
              </div>

              {/* Example Calculation */}
              {explanation.course_breakdown && explanation.course_breakdown.length > 0 && (
                <div className="border-2 border-emerald-200 rounded-xl p-5 bg-gradient-to-br from-emerald-50 to-white">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-8 h-8 bg-emerald-600 text-white rounded-full flex items-center justify-center font-bold">📋</div>
                    <h4 className="font-bold text-lg text-slate-900">Example: How One Course Contributed</h4>
                  </div>
                  <p className="text-sm text-slate-700 mb-4">
                    Let's trace how <strong className="text-emerald-700">{explanation.course_breakdown[0].course_code}</strong> contributed to your final score:
                  </p>
                  <div className="bg-white border-2 border-emerald-300 rounded-lg p-5 space-y-4">
                    {/* Course Details */}
                    <div className="grid grid-cols-2 gap-4 bg-emerald-50 p-3 rounded-lg">
                      <div>
                        <span className="text-xs text-slate-600 block">Your Grade</span>
                        <span className="text-xl font-bold text-emerald-700">{explanation.course_breakdown[0].grade}</span>
                      </div>
                      <div>
                        <span className="text-xs text-slate-600 block">Course Weight</span>
                        <span className="text-xl font-bold text-emerald-700">{explanation.course_breakdown[0].weight}</span>
                      </div>
                    </div>

                    {/* Step-by-step calculation for this course */}
                    <div className="space-y-3">
                      <div className="bg-gradient-to-r from-emerald-100 to-teal-50 p-4 rounded-lg border-l-4 border-emerald-500">
                        <div className="text-xs font-semibold text-emerald-800 mb-2">STEP 1: Grade → Points</div>
                        <div className="font-mono text-sm text-emerald-900">
                          Grade {explanation.course_breakdown[0].grade} = {explanation.course_breakdown[0].grade} points
                        </div>
                        <div className="text-xs text-emerald-700 mt-1">
                          (Letter grades are converted to numerical values)
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-emerald-100 to-teal-50 p-4 rounded-lg border-l-4 border-emerald-500">
                        <div className="text-xs font-semibold text-emerald-800 mb-2">STEP 2: Calculate Weighted Contribution</div>
                        <div className="font-mono text-sm text-emerald-900 mb-2">
                          Contribution = Grade Points × Weight
                        </div>
                        <div className="font-mono text-sm text-emerald-900 font-bold">
                          Contribution = {explanation.course_breakdown[0].grade} × {explanation.course_breakdown[0].weight}
                        </div>
                        <div className="font-mono text-lg text-emerald-900 font-bold mt-2 bg-white px-3 py-2 rounded border border-emerald-300">
                          Contribution = {explanation.course_breakdown[0].contribution}
                        </div>
                      </div>

                      <div className="bg-gradient-to-r from-blue-100 to-indigo-50 p-4 rounded-lg border-l-4 border-blue-500">
                        <div className="text-xs font-semibold text-blue-800 mb-2">📊 This Course's Impact</div>
                        <div className="text-sm text-blue-900">
                          This course added <strong className="text-lg text-blue-700">{explanation.course_breakdown[0].contribution}</strong> to your total contribution of{' '}
                          <strong className="text-lg text-blue-700">{explanation.calculation.total_contribution}</strong>
                        </div>
                        <div className="mt-2 text-xs text-blue-700">
                          That's {((parseFloat(explanation.course_breakdown[0].contribution) / parseFloat(explanation.calculation.total_contribution)) * 100).toFixed(1)}% of your total score!
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Your Score Summary */}
              <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-300 rounded-xl p-5">
                <div className="flex items-start gap-3">
                  <Info className="w-6 h-6 text-amber-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <div className="text-base font-bold text-amber-900 mb-2">Your Final Score: {explanation.score}%</div>
                    <p className="text-sm text-amber-800">
                      This means you've demonstrated <strong>{explanation.level}</strong> level proficiency in{' '}
                      <strong>{explanation.skill_name}</strong> based on your performance in{' '}
                      <strong>{explanation.summary.total_courses}</strong> related course{explanation.summary.total_courses !== 1 ? 's' : ''},{' '}
                      covering <strong>{explanation.summary.unique_child_skills}</strong> specific skill{explanation.summary.unique_child_skills !== 1 ? 's' : ''}.
                    </p>
                    <div className="mt-3 flex items-center gap-2">
                      <div className="text-sm text-amber-700">
                        📊 Total Contribution: <strong>{explanation.calculation.total_contribution}</strong>
                      </div>
                      <div className="text-sm text-amber-700">
                        ⚖️ Total Weight: <strong>{explanation.calculation.total_weight}</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Confidence Score */}
            <div className="border-t border-slate-200 pt-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm text-slate-600 mb-1">Confidence Level</div>
                  <div className="text-2xl font-bold text-slate-900">
                    {(explanation.confidence * 100).toFixed(1)}%
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    How reliable this score is based on available data
                  </p>
                </div>
                <div className="text-right">
                  <div className="w-32 h-32">
                    <svg viewBox="0 0 100 100" className="transform -rotate-90">
                      <circle cx="50" cy="50" r="40" fill="none" stroke="#e5e7eb" strokeWidth="8"/>
                      <circle 
                        cx="50" 
                        cy="50" 
                        r="40" 
                        fill="none" 
                        stroke="#3b82f6" 
                        strokeWidth="8"
                        strokeDasharray={`${explanation.confidence * 251.2} 251.2`}
                        strokeLinecap="round"
                      />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-blue-200 shadow-md hover:shadow-lg transition-shadow">
            <CardContent className="text-center py-8 bg-gradient-to-br from-blue-50 to-blue-100">
              <BookOpen className="w-12 h-12 text-blue-600 mx-auto mb-3" />
              <div className="text-4xl font-bold text-blue-900 mb-1">{explanation.summary.total_courses}</div>
              <div className="text-sm font-semibold text-blue-700">Contributing Courses</div>
              <div className="text-xs text-blue-600 mt-1">Academic evidence</div>
            </CardContent>
          </Card>
          <Card className="border-green-200 shadow-md hover:shadow-lg transition-shadow">
            <CardContent className="text-center py-8 bg-gradient-to-br from-green-50 to-green-100">
              <Award className="w-12 h-12 text-green-600 mx-auto mb-3" />
              <div className="text-4xl font-bold text-green-900 mb-1">{explanation.summary.unique_child_skills}</div>
              <div className="text-sm font-semibold text-green-700">Related Skills</div>
              <div className="text-xs text-green-600 mt-1">Covered topics</div>
            </CardContent>
          </Card>
          <Card className="border-purple-200 shadow-md hover:shadow-lg transition-shadow">
            <CardContent className="text-center py-8 bg-gradient-to-br from-purple-50 to-purple-100">
              <TrendingUp className="w-12 h-12 text-purple-600 mx-auto mb-3" />
              <div className="text-base font-bold text-purple-900 mb-1 truncate px-2 min-h-[2.5rem] flex items-center justify-center">
                {explanation.summary.strongest_contributor || 'N/A'}
              </div>
              <div className="text-sm font-semibold text-purple-700">Top Contributor</div>
              <div className="text-xs text-purple-600 mt-1">Highest impact skill</div>
            </CardContent>
          </Card>
        </div>

        <Card className="shadow-md">
          <CardHeader className="bg-slate-50">
            <h2 className="text-xl font-semibold">What Contributed to This Score?</h2>
            <p className="text-sm text-slate-600 mt-1">
              Each course and skill below added to your total score
            </p>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="space-y-4">
              {explanation.child_skills.map((skill, idx) => (
                <div key={idx} className="border-2 border-slate-200 rounded-xl p-5 hover:border-blue-300 hover:shadow-md transition-all">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="font-bold text-lg text-slate-900">{skill.child_skill}</h3>
                      <div className="flex items-center gap-4 mt-2 text-sm text-slate-600">
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-4 h-4" />
                          {skill.course_count} course{skill.course_count !== 1 ? 's' : ''}
                        </span>
                        <span className="font-medium text-blue-600">
                          {skill.contribution_percentage.toFixed(1)}% of your total score
                        </span>
                      </div>
                    </div>
                    <div className="text-right bg-blue-50 px-4 py-2 rounded-lg border-2 border-blue-200">
                      <div className="text-xs text-blue-700 font-semibold">CONTRIBUTION</div>
                      <div className="text-2xl font-bold text-blue-600">
                        {skill.contribution_percentage.toFixed(1)}%
                      </div>
                    </div>
                  </div>
                  
                  <div className="mb-4">
                    <div className="flex items-center justify-between text-xs text-slate-600 mb-1">
                      <span>Impact on total score</span>
                      <span className="font-medium">{skill.contribution_percentage.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-3 overflow-hidden">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-indigo-500 h-3 rounded-full transition-all duration-500 shadow-inner"
                        style={{ width: `${Math.min(skill.contribution_percentage, 100)}%` }}
                      />
                    </div>
                  </div>

                  <details className="text-sm group">
                    <summary className="cursor-pointer text-blue-600 hover:text-blue-700 font-semibold py-2 px-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors flex items-center justify-between">
                      <span>📚 View detailed breakdown ({skill.course_count} course{skill.course_count !== 1 ? 's' : ''})</span>
                      <ChevronDown className="w-4 h-4 group-open:rotate-180 transition-transform" />
                    </summary>
                    <div className="mt-4 space-y-3 pl-2">
                      {skill.courses.map((course, courseIdx) => (
                        <div key={courseIdx} className="bg-gradient-to-r from-slate-50 to-white p-4 rounded-lg border-l-4 border-blue-400 shadow-sm">
                          <div className="flex justify-between items-start mb-3">
                            <div className="flex-1">
                              <div className="font-bold text-slate-900 text-base">{course.course_code}</div>
                              <div className="flex items-center gap-3 mt-1 text-sm">
                                <span className="px-2 py-1 bg-green-100 text-green-700 rounded font-semibold">
                                  Grade: {course.grade}
                                </span>
                                <span className="text-slate-600">{course.credits} credits</span>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="text-sm text-slate-600">Contribution</div>
                              <div className="text-xl font-bold text-blue-600">
                                {course.contribution}
                              </div>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-3 gap-3 mt-3 pt-3 border-t border-slate-200">
                            <div className="text-center">
                              <div className="text-xs text-slate-500">Weight</div>
                              <div className="font-semibold text-slate-900">{course.weight}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-xs text-slate-500">Recency</div>
                              <div className="font-semibold text-slate-900">{course.recency}</div>
                            </div>
                            <div className="text-center">
                              <div className="text-xs text-slate-500">Map Weight</div>
                              <div className="font-semibold text-slate-900">{course.map_weight}</div>
                            </div>
                          </div>

                          <div className="mt-3 pt-3 border-t border-slate-200 bg-blue-50 -m-4 p-3 rounded-b-lg">
                            <div className="text-xs text-slate-600 font-medium mb-1">How this course contributed:</div>
                            <div className="text-xs text-slate-700 font-mono bg-white p-2 rounded">
                              Grade ({course.grade}) × Weight ({course.weight}) = Contribution ({course.contribution})
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="shadow-md">
          <CardHeader className="bg-slate-50">
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <Award className="w-6 h-6 text-slate-700" />
              Complete Course Breakdown
            </h2>
            <p className="text-sm text-slate-600 mt-1">
              All courses that contributed to this skill score
            </p>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-slate-100 to-slate-50 border-b-2 border-slate-300">
                  <tr>
                    <th className="text-left py-4 px-4 text-sm font-bold text-slate-800">Course Code</th>
                    <th className="text-left py-4 px-4 text-sm font-bold text-slate-800">Related Skill</th>
                    <th className="text-center py-4 px-4 text-sm font-bold text-slate-800">Grade</th>
                    <th className="text-right py-4 px-4 text-sm font-bold text-slate-800">Contribution</th>
                    <th className="text-right py-4 px-4 text-sm font-bold text-slate-800">Weight</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {explanation.course_breakdown.map((course, idx) => (
                    <tr key={idx} className="hover:bg-blue-50 transition-colors">
                      <td className="py-4 px-4 font-bold text-slate-900">{course.course_code}</td>
                      <td className="py-4 px-4 text-sm text-slate-700">{course.child_skill}</td>
                      <td className="py-4 px-4 text-center">
                        <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full font-semibold text-sm">
                          {course.grade}
                        </span>
                      </td>
                      <td className="py-4 px-4 text-right font-bold text-blue-600 text-lg">{course.contribution}</td>
                      <td className="py-4 px-4 text-right text-slate-600 font-medium">{course.weight}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="bg-slate-100 border-t-2 border-slate-300">
                  <tr>
                    <td colSpan="3" className="py-4 px-4 text-right font-bold text-slate-800">TOTALS:</td>
                    <td className="py-4 px-4 text-right font-bold text-blue-700 text-xl">
                      {explanation.calculation.total_contribution}
                    </td>
                    <td className="py-4 px-4 text-right font-bold text-slate-700 text-xl">
                      {explanation.calculation.total_weight}
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
            
            <div className="mt-6 space-y-4">
              {/* Summary of totals */}
              <div className="bg-gradient-to-r from-slate-100 to-slate-50 p-4 rounded-lg border-2 border-slate-300">
                <div className="text-sm font-bold text-slate-800 mb-3 flex items-center gap-2">
                  <div className="w-6 h-6 bg-slate-600 text-white rounded-full flex items-center justify-center text-xs">Σ</div>
                  Summary of All Contributions
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-3 rounded-lg border border-slate-300">
                    <div className="text-xs text-slate-600">Sum of All Contributions</div>
                    <div className="text-3xl font-bold text-blue-700">{explanation.calculation.total_contribution}</div>
                    <div className="text-xs text-slate-500 mt-1">All courses' Grade × Weight</div>
                  </div>
                  <div className="bg-white p-3 rounded-lg border border-slate-300">
                    <div className="text-xs text-slate-600">Sum of All Weights</div>
                    <div className="text-3xl font-bold text-purple-700">{explanation.calculation.total_weight}</div>
                    <div className="text-xs text-slate-500 mt-1">Total importance factor</div>
                  </div>
                </div>
              </div>

              {/* Final formula with actual numbers */}
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-xl shadow-lg">
                <div className="text-sm font-semibold mb-4 text-center opacity-90">🎯 FINAL SCORE CALCULATION</div>
                
                <div className="space-y-3">
                  {/* Formula */}
                  <div className="bg-white/10 rounded-lg p-3 text-center">
                    <div className="text-xs opacity-80">Formula:</div>
                    <div className="font-mono text-base font-bold mt-1">
                      Score = (Total Contribution ÷ Total Weight) × 100
                    </div>
                  </div>

                  {/* With values */}
                  <div className="bg-white/15 rounded-lg p-3 text-center">
                    <div className="text-xs opacity-80">Substituting values:</div>
                    <div className="font-mono text-lg font-bold mt-1">
                      Score = ({explanation.calculation.total_contribution} ÷ {explanation.calculation.total_weight}) × 100
                    </div>
                  </div>

                  {/* Calculation */}
                  <div className="bg-white/20 rounded-lg p-3 text-center">
                    <div className="text-xs opacity-80">Calculating:</div>
                    <div className="font-mono text-lg font-bold mt-1">
                      Score = {(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)} × 100
                    </div>
                  </div>

                  {/* Result */}
                  <div className="bg-yellow-400 text-blue-900 rounded-lg p-4 text-center border-2 border-yellow-300">
                    <div className="text-xs font-semibold">YOUR FINAL SCORE:</div>
                    <div className="font-mono text-4xl font-bold mt-1">
                      {explanation.score}%
                    </div>
                  </div>
                </div>

                {/* Verification */}
                <div className="mt-4 pt-4 border-t border-white/30 text-center">
                  <div className="text-xs opacity-80">Verification:</div>
                  <div className="font-mono text-sm mt-1">
                    {explanation.calculation.total_contribution} ÷ {explanation.calculation.total_weight} = {(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)}
                  </div>
                  <div className="font-mono text-sm">
                    {(explanation.calculation.total_contribution / explanation.calculation.total_weight).toFixed(4)} × 100 = {explanation.score}%
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
