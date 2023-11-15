using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ApplyTransforms : MonoBehaviour
{
    [SerializeField] Vector3 displacement;
    [SerializeField]float angle;
    [SerializeField]AXIS rotationAxis;
    [SerializeField] GameObject wheel1;
    [SerializeField] GameObject wheel2;
    [SerializeField] GameObject wheel3;
    [SerializeField] GameObject wheel4;

    Mesh [] mesh;
    Mesh wheel1Mesh;
    Mesh wheel2Mesh;
    Mesh wheel3Mesh;
    Mesh wheel4Mesh;

    Vector3[] baseVertices;
    Vector3[] newVertices;

    Vector3[] spoilerVertices;
    Vector3[] spoilerNewVertices;
    Vector3[] wheel1Vertices;
    Vector3[] wheel1NewVertices;
    Vector3[] wheel2Vertices;
    Vector3[] wheel2NewVertices;
    Vector3[] wheel3Vertices;
    Vector3[] wheel3NewVertices;
    Vector3[] wheel4Vertices;
    Vector3[] wheel4NewVertices;
    // Start is called before the first frame update
    void Start()
    {
        MeshFilter [] meshfilters = GetComponentsInChildren<MeshFilter>();
        mesh = new Mesh[meshfilters.Length];
        for (int i = 0; i < meshfilters.Length; i++)
        {
            mesh[i] = meshfilters[i].mesh;
        }
        wheel1Mesh = wheel1.GetComponentInChildren<MeshFilter>().mesh;
        wheel2Mesh = wheel2.GetComponentInChildren<MeshFilter>().mesh;
        wheel3Mesh = wheel3.GetComponentInChildren<MeshFilter>().mesh;
        wheel4Mesh = wheel4.GetComponentInChildren<MeshFilter>().mesh;

        baseVertices = mesh[0].vertices;
        spoilerVertices = mesh[1].vertices;
        wheel1Vertices = wheel1Mesh.vertices;
        wheel2Vertices = wheel2Mesh.vertices;
        wheel3Vertices = wheel3Mesh.vertices;
        wheel4Vertices = wheel4Mesh.vertices;

        newVertices = new Vector3[baseVertices.Length];
        for (int i = 0; i < baseVertices.Length; i++)
        {
            newVertices[i] = baseVertices[i];
        }

        spoilerNewVertices = new Vector3[spoilerVertices.Length];
        for (int i = 0; i < spoilerVertices.Length; i++)
        {
            spoilerNewVertices[i] = spoilerVertices[i];
        }

        wheel1NewVertices = new Vector3[wheel1Vertices.Length];
        for (int i = 0; i < wheel1Vertices.Length; i++)
        {
            wheel1NewVertices[i] = wheel1Vertices[i];
        }

        wheel2NewVertices = new Vector3[wheel2Vertices.Length];
        for (int i = 0; i < wheel2Vertices.Length; i++)
        {
            wheel2NewVertices[i] = wheel2Vertices[i];
        }

        wheel3NewVertices = new Vector3[wheel3Vertices.Length];
        for (int i = 0; i < wheel3Vertices.Length; i++)
        {
            wheel3NewVertices[i] = wheel3Vertices[i];
        }

        wheel4NewVertices = new Vector3[wheel4Vertices.Length];
        for (int i = 0; i < wheel4Vertices.Length; i++)
        {
            wheel4NewVertices[i] = wheel4Vertices[i];
        }
        
        
        
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform(){
        //create the matrices

        // Calculate the angle in radians
        float angleRadians = Mathf.Atan2(displacement.z, displacement.x);

        // Convert the angle to degrees
        float angleDegrees = angleRadians * Mathf.Rad2Deg -90;
        Matrix4x4 move= HW_Transforms.TranslationMat(displacement.x *Time.time , displacement.y *Time.time, displacement.z *Time.time);
        Matrix4x4 moveOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);
        Matrix4x4 moveObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);
        Matrix4x4 rotate = HW_Transforms.RotateMat(angleDegrees  , rotationAxis);
        
        Matrix4x4 spoilerMove = HW_Transforms.TranslationMat(0,1.05f,-2.31f);

        Matrix4x4 moveWheel1 = HW_Transforms.TranslationMat(0.9f,0.35f,1.5f);
        Matrix4x4 moveWheel2 = HW_Transforms.TranslationMat(-0.9f,0.35f,1.5f);
        // Matrix4x4 rotateWheel = HW_Transforms.RotateMat(90, AXIS.X);

        Matrix4x4 moveWheel3 = HW_Transforms.TranslationMat(0.9f,0.35f,-1.4f);
        Matrix4x4 moveWheel4 = HW_Transforms.TranslationMat(-0.9f,0.35f,-1.4f);
        Matrix4x4 scaleWheel = HW_Transforms.ScaleMat(.2f,.2f,.2f);

        Matrix4x4 rotateWheelinOrigin = HW_Transforms.RotateMat(-90*Time.time, AXIS.X);
        

        //combine the matrices
        //operations are executed in backwards order
        Matrix4x4 composite =  move * rotate;

        // for (int i=0; i<newVertices.Length; i++)
        // {
        //     Vector4 temp = new Vector4(newVertices[i].x, newVertices[i].y, newVertices[i].z, 1);

        //     newVertices[i] = composite * temp;
        // }
        for (int i=0; i<newVertices.Length; i++)
        {
            Vector4 temp = new Vector4(baseVertices[i].x, baseVertices[i].y, baseVertices[i].z, 1);

            newVertices[i] = composite * temp;
        }

        for (int i = 0; i<spoilerNewVertices.Length; i++)
        {
            Vector4 temp = new Vector4(spoilerVertices[i].x, spoilerVertices[i].y, spoilerVertices[i].z, 1);

            spoilerNewVertices[i] = composite * spoilerMove *temp;
        }

        for(int i = 0; i<wheel1NewVertices.Length; i++)
        {
            Vector4 temp1 = new Vector4(wheel1Vertices[i].x, wheel1Vertices[i].y, wheel1Vertices[i].z, 1);

            wheel1NewVertices[i] = composite * moveWheel1 *rotateWheelinOrigin* scaleWheel * temp1;
        }

        for(int i = 0; i<wheel2NewVertices.Length; i++)
        {
            Vector4 temp2 = new Vector4(wheel2Vertices[i].x, wheel2Vertices[i].y, wheel2Vertices[i].z, 1);

            wheel2NewVertices[i] = composite * moveWheel2 * rotateWheelinOrigin*scaleWheel *temp2;
        }

        for(int i = 0; i<wheel3NewVertices.Length; i++)
        {
            Vector4 temp3 = new Vector4(wheel3Vertices[i].x, wheel3Vertices[i].y, wheel3Vertices[i].z, 1);

            wheel3NewVertices[i] = composite  * moveWheel3* rotateWheelinOrigin * scaleWheel *temp3;
        }

        for(int i = 0; i<wheel4NewVertices.Length; i++)
        {
            Vector4 temp4 = new Vector4(wheel4Vertices[i].x, wheel4Vertices[i].y, wheel4Vertices[i].z, 1);

            wheel4NewVertices[i] = composite * moveWheel4* rotateWheelinOrigin* scaleWheel*temp4;
        }


        mesh[0].vertices = newVertices;
        mesh[1].vertices = spoilerNewVertices;
        wheel1Mesh.vertices = wheel1NewVertices;
        wheel2Mesh.vertices = wheel2NewVertices;
        wheel3Mesh.vertices = wheel3NewVertices;
        wheel4Mesh.vertices = wheel4NewVertices;
        mesh[0].RecalculateNormals();
        mesh[1].RecalculateNormals();
        wheel1Mesh.RecalculateNormals();
        wheel2Mesh.RecalculateNormals();
        wheel3Mesh.RecalculateNormals();
        wheel4Mesh.RecalculateNormals();

    
    }
}
