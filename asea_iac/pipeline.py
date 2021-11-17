from aws_cdk import (
    core as cdk,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_codecommit as codecommit,
    pipelines as pipelines,
    aws_iam as iam,
    aws_codebuild as codebuild
)

class EKSStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # REPO
        repo = codecommit.Repository(self, "IAC",
        repository_name="IAC",
        description="CDK IAC Pipeline."
        )

        # PIPELINE
        source_artifact = codepipeline.Artifact()
        
        pipeline = pipelines.CodePipeline(self, "Pipeline", 
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "master"),
                commands=["pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"]
            ),
        
        code_build_defaults=pipelines.CodeBuildOptions(
            build_environment=codebuild.BuildEnvironment(privileged=True),
            role_policy=[iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["cloudformation:*"],
                        resources=["*"],
                    )
                ]
        )
        )
