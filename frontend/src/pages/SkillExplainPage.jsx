import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Spinner } from '../components/ui/Spinner';
import { ErrorAlert } from '../components/ui/ErrorAlert';
import { getSkillExplanation } from '../api/api';
import { ChevronLeft, Info, TrendingUp, BookOpen, Award } from 'lucide-react';

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

        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              How This Score Was Calculated
            </h2>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-slate-600">Total Contribution</div>
                  <div className="text-2xl font-bold text-slate-900">
                    {explanation.calculation.total_contribution}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-slate-600">Total Weight</div>
                  <div className="text-2xl font-bold text-slate-900">
                    {explanation.calculation.total_weight}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-slate-600">Confidence</div>
                  <div className="text-2xl font-bold text-slate-900">
                    {(explanation.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg border border-blue-100">
                <div className="text-sm font-medium text-blue-900 mb-2">Formula</div>
                <div className="font-mono text-sm text-blue-800 space-y-1">
                  <div>{explanation.calculation.formula}</div>
                  <div className="text-xs text-blue-600 mt-2">
                    {explanation.calculation.confidence_formula}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card>
            <CardContent className="text-center py-6">
              <BookOpen className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="text-3xl font-bold text-slate-900">{explanation.summary.total_courses}</div>
              <div className="text-sm text-slate-600">Contributing Courses</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="text-center py-6">
              <Award className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <div className="text-3xl font-bold text-slate-900">{explanation.summary.unique_child_skills}</div>
              <div className="text-sm text-slate-600">Related Skills</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="text-center py-6">
              <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <div className="text-lg font-bold text-slate-900 truncate px-2">
                {explanation.summary.strongest_contributor || 'N/A'}
              </div>
              <div className="text-sm text-slate-600">Top Contributor</div>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">Contributing Skills Breakdown</h2>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {explanation.child_skills.map((skill, idx) => (
                <div key={idx} className="border border-slate-200 rounded-lg p-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <h3 className="font-semibold text-slate-900">{skill.child_skill}</h3>
                      <div className="text-sm text-slate-600 mt-1">
                        {skill.course_count} course{skill.course_count !== 1 ? 's' : ''}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-blue-600">
                        {skill.contribution_percentage.toFixed(1)}%
                      </div>
                      <div className="text-xs text-slate-500">of total</div>
                    </div>
                  </div>
                  
                  <div className="w-full bg-slate-200 rounded-full h-2 mb-3">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${skill.contribution_percentage}%` }}
                    />
                  </div>

                  <details className="text-sm">
                    <summary className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium">
                      View {skill.course_count} course{skill.course_count !== 1 ? 's' : ''}
                    </summary>
                    <div className="mt-3 space-y-2">
                      {skill.courses.map((course, courseIdx) => (
                        <div key={courseIdx} className="bg-white p-3 rounded border border-slate-200">
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="font-medium text-slate-900">{course.course_code}</span>
                              <span className="text-slate-600 ml-2">Grade: {course.grade}</span>
                            </div>
                            <div className="text-right text-sm">
                              <div className="font-medium text-slate-900">
                                Contribution: {course.contribution}
                              </div>
                              <div className="text-slate-500">
                                Weight: {course.weight}
                              </div>
                            </div>
                          </div>
                          <div className="mt-2 grid grid-cols-3 gap-2 text-xs text-slate-600">
                            <div>Credits: {course.credits}</div>
                            <div>Recency: {course.recency}</div>
                            <div>Map Weight: {course.map_weight}</div>
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

        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">All Contributing Courses</h2>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Course</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-slate-700">Via Skill</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-slate-700">Grade</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-slate-700">Contribution</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-slate-700">Weight</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {explanation.course_breakdown.map((course, idx) => (
                    <tr key={idx} className="hover:bg-slate-50">
                      <td className="py-3 px-4 font-medium text-slate-900">{course.course_code}</td>
                      <td className="py-3 px-4 text-sm text-slate-600">{course.child_skill}</td>
                      <td className="py-3 px-4 text-right font-medium">{course.grade}</td>
                      <td className="py-3 px-4 text-right font-medium text-blue-600">{course.contribution}</td>
                      <td className="py-3 px-4 text-right text-slate-600">{course.weight}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
