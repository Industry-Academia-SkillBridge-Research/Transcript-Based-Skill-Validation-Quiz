import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CheckCircle2, ArrowRight, Briefcase } from "lucide-react";
import { getClaimedSkills, planQuiz } from "@/api/api";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/Table";
import { ErrorAlert } from "@/components/ui/ErrorAlert";
import { Spinner } from "@/components/ui/Spinner";

export default function SkillsPage() {
  const navigate = useNavigate();
  const { studentId } = useParams();
  const [skills, setSkills] = useState([]);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSkills = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await getClaimedSkills(studentId);
        // Extract job skill scores from the API response
        const jobSkills = data.job_skill_scores || [];
        setSkills(jobSkills);
      } catch (err) {
        setError(err.response?.data || { message: err.message });
      } finally {
        setLoading(false);
      }
    };

    fetchSkills();
  }, [studentId]);

  const handleSkillToggle = (skillName) => {
    setSelectedSkills((prev) => {
      if (prev.includes(skillName)) {
        return prev.filter((s) => s !== skillName);
      } else {
        if (prev.length >= 5) {
          setError({ message: "You can select up to 5 skills only" });
          return prev;
        }
        setError(null);
        return [...prev, skillName];
      }
    });
  };

  const handlePlanQuiz = async () => {
    if (selectedSkills.length === 0) {
      setError({ message: "Please select at least one skill" });
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await planQuiz(studentId, selectedSkills);
      navigate(`/students/${studentId}/quiz`);
    } catch (err) {
      setError(err.response?.data || { message: err.message });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="container mx-auto max-w-6xl p-6 space-y-6">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-foreground mb-2">Your Skills Portfolio</h2>
        <p className="text-muted-foreground">Select skills to validate through personalized quizzes</p>
      </div>
      
      <Card className="border-primary/20">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <CheckCircle2 className="h-6 w-6" />
            Claimed Skills
          </CardTitle>
          <CardDescription>
            Select up to 5 skills to validate through a quiz
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {error && <ErrorAlert error={error} />}
          
          <div className="bg-gradient-to-r from-primary/10 to-primary/5 p-4 rounded-xl border border-primary/20">
            <p className="text-sm font-semibold text-foreground mb-2">
              Selected: <span className="text-primary text-lg">{selectedSkills.length}</span> / 5 skills
            </p>
            <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-primary to-primary-dark transition-all duration-300"
                style={{ width: `${(selectedSkills.length / 5) * 100}%` }}
              />
            </div>
          </div>

          {skills.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-12">Select</TableHead>
                  <TableHead>Job Skill</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Level</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {skills.map((skill, index) => {
                  const level = skill.score >= 80 ? 'Advanced' : skill.score >= 60 ? 'Intermediate' : 'Beginner';
                  const skillName = skill.job_skill_name || skill.skill_name || skill.job_skill_id;
                  return (
                    <TableRow key={index}>
                      <TableCell>
                        <input
                          type="checkbox"
                          checked={selectedSkills.includes(skillName)}
                          onChange={() => handleSkillToggle(skillName)}
                          className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary cursor-pointer"
                          disabled={
                            !selectedSkills.includes(skillName) &&
                            selectedSkills.length >= 5
                          }
                        />
                      </TableCell>
                      <TableCell className="font-medium">{skillName}</TableCell>
                      <TableCell>
                        <span className="inline-flex items-center rounded-full px-2 py-1 text-xs font-medium bg-purple-100 text-purple-700">
                          {skill.category}
                        </span>
                      </TableCell>
                      <TableCell>
                        <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                          level === 'Advanced' ? 'bg-green-100 text-green-700' :
                          level === 'Intermediate' ? 'bg-blue-100 text-blue-700' :
                          'bg-red-100 text-red-700'
                        }`}>
                          {level}
                        </span>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          ) : (
            <p className="text-sm text-muted-foreground">No skills found</p>
          )}
        </CardContent>
      </Card>

      <div className="flex justify-end pt-2 gap-3">
        <Button
          variant="outline"
          onClick={() => navigate(`/students/${studentId}/jobs`)}
          className="gap-2"
          size="lg"
        >
          <Briefcase className="h-5 w-5" />
          View Job Matches
        </Button>
        {submitting ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Spinner className="h-5 w-5" />
            <span>Planning quiz...</span>
          </div>
        ) : (
          <Button
            onClick={handlePlanQuiz}
            disabled={selectedSkills.length === 0}
            className="gap-2"
            size="lg"
          >
            Plan Quiz
            <ArrowRight className="h-5 w-5" />
          </Button>
        )}
      </div>
    </div>
  );
}
