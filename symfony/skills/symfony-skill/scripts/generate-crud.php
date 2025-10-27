#!/usr/bin/env php
<?php
/**
 * Symfony CRUD Generator Script
 * 
 * Usage: php generate-crud.php EntityName [--api]
 * Example: php generate-crud.php Product
 */

if ($argc < 2) {
    echo "Usage: php generate-crud.php EntityName [--api]\n";
    exit(1);
}

$entityName = $argv[1];
$isApi = in_array('--api', $argv);
$entityLower = strtolower($entityName);
$entityPlural = $entityLower . 's';

// Generate Controller
if (!$isApi) {
    $controllerCode = "<?php

namespace App\Controller;

use App\Entity\\$entityName;
use App\Form\\{$entityName}Type;
use App\Repository\\{$entityName}Repository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/$entityPlural')]
class {$entityName}Controller extends AbstractController
{
    #[Route('/', name: '{$entityLower}_index', methods: ['GET'])]
    public function index({$entityName}Repository \$repository): Response
    {
        return \$this->render('{$entityLower}/index.html.twig', [
            '{$entityPlural}' => \$repository->findAll(),
        ]);
    }

    #[Route('/new', name: '{$entityLower}_new', methods: ['GET', 'POST'])]
    public function new(Request \$request, EntityManagerInterface \$entityManager): Response
    {
        \${$entityLower} = new $entityName();
        \$form = \$this->createForm({$entityName}Type::class, \${$entityLower});
        \$form->handleRequest(\$request);

        if (\$form->isSubmitted() && \$form->isValid()) {
            \$entityManager->persist(\${$entityLower});
            \$entityManager->flush();

            \$this->addFlash('success', '$entityName created successfully!');

            return \$this->redirectToRoute('{$entityLower}_show', ['id' => \${$entityLower}->getId()]);
        }

        return \$this->render('{$entityLower}/new.html.twig', [
            '{$entityLower}' => \${$entityLower},
            'form' => \$form,
        ]);
    }

    #[Route('/{id}', name: '{$entityLower}_show', methods: ['GET'])]
    public function show($entityName \${$entityLower}): Response
    {
        return \$this->render('{$entityLower}/show.html.twig', [
            '{$entityLower}' => \${$entityLower},
        ]);
    }

    #[Route('/{id}/edit', name: '{$entityLower}_edit', methods: ['GET', 'POST'])]
    public function edit(Request \$request, $entityName \${$entityLower}, EntityManagerInterface \$entityManager): Response
    {
        \$form = \$this->createForm({$entityName}Type::class, \${$entityLower});
        \$form->handleRequest(\$request);

        if (\$form->isSubmitted() && \$form->isValid()) {
            \$entityManager->flush();

            \$this->addFlash('success', '$entityName updated successfully!');

            return \$this->redirectToRoute('{$entityLower}_show', ['id' => \${$entityLower}->getId()]);
        }

        return \$this->render('{$entityLower}/edit.html.twig', [
            '{$entityLower}' => \${$entityLower},
            'form' => \$form,
        ]);
    }

    #[Route('/{id}', name: '{$entityLower}_delete', methods: ['POST'])]
    public function delete(Request \$request, $entityName \${$entityLower}, EntityManagerInterface \$entityManager): Response
    {
        if (\$this->isCsrfTokenValid('delete'.\${$entityLower}->getId(), \$request->request->get('_token'))) {
            \$entityManager->remove(\${$entityLower});
            \$entityManager->flush();

            \$this->addFlash('success', '$entityName deleted successfully!');
        }

        return \$this->redirectToRoute('{$entityLower}_index');
    }
}
";
} else {
    // API Controller
    $controllerCode = "<?php

namespace App\Controller\Api;

use App\Entity\\$entityName;
use App\Repository\\{$entityName}Repository;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Serializer\SerializerInterface;
use Symfony\Component\Validator\Validator\ValidatorInterface;

#[Route('/api/{$entityPlural}')]
class {$entityName}ApiController extends AbstractController
{
    public function __construct(
        private EntityManagerInterface \$entityManager,
        private SerializerInterface \$serializer,
        private ValidatorInterface \$validator
    ) {}

    #[Route('', name: 'api_{$entityLower}_index', methods: ['GET'])]
    public function index({$entityName}Repository \$repository): JsonResponse
    {
        \${$entityPlural} = \$repository->findAll();
        
        return \$this->json(\${$entityPlural}, Response::HTTP_OK, [], [
            'groups' => ['{$entityLower}:read']
        ]);
    }

    #[Route('', name: 'api_{$entityLower}_create', methods: ['POST'])]
    public function create(Request \$request): JsonResponse
    {
        \${$entityLower} = \$this->serializer->deserialize(
            \$request->getContent(),
            $entityName::class,
            'json'
        );

        \$errors = \$this->validator->validate(\${$entityLower});
        
        if (count(\$errors) > 0) {
            \$errorMessages = [];
            foreach (\$errors as \$error) {
                \$errorMessages[\$error->getPropertyPath()] = \$error->getMessage();
            }
            
            return \$this->json([
                'errors' => \$errorMessages
            ], Response::HTTP_BAD_REQUEST);
        }

        \$this->entityManager->persist(\${$entityLower});
        \$this->entityManager->flush();

        return \$this->json(\${$entityLower}, Response::HTTP_CREATED, [], [
            'groups' => ['{$entityLower}:read']
        ]);
    }

    #[Route('/{id}', name: 'api_{$entityLower}_show', methods: ['GET'])]
    public function show($entityName \${$entityLower}): JsonResponse
    {
        return \$this->json(\${$entityLower}, Response::HTTP_OK, [], [
            'groups' => ['{$entityLower}:read', '{$entityLower}:detail']
        ]);
    }

    #[Route('/{id}', name: 'api_{$entityLower}_update', methods: ['PUT'])]
    public function update(Request \$request, $entityName \${$entityLower}): JsonResponse
    {
        \$data = json_decode(\$request->getContent(), true);
        
        \$this->serializer->deserialize(
            \$request->getContent(),
            $entityName::class,
            'json',
            ['object_to_populate' => \${$entityLower}]
        );

        \$errors = \$this->validator->validate(\${$entityLower});
        
        if (count(\$errors) > 0) {
            \$errorMessages = [];
            foreach (\$errors as \$error) {
                \$errorMessages[\$error->getPropertyPath()] = \$error->getMessage();
            }
            
            return \$this->json([
                'errors' => \$errorMessages
            ], Response::HTTP_BAD_REQUEST);
        }

        \$this->entityManager->flush();

        return \$this->json(\${$entityLower}, Response::HTTP_OK, [], [
            'groups' => ['{$entityLower}:read']
        ]);
    }

    #[Route('/{id}', name: 'api_{$entityLower}_delete', methods: ['DELETE'])]
    public function delete($entityName \${$entityLower}): JsonResponse
    {
        \$this->entityManager->remove(\${$entityLower});
        \$this->entityManager->flush();

        return \$this->json(null, Response::HTTP_NO_CONTENT);
    }
}
";
}

// Generate Form Type
$formCode = "<?php

namespace App\Form;

use App\Entity\\$entityName;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\Extension\Core\Type\NumberType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

class {$entityName}Type extends AbstractType
{
    public function buildForm(FormBuilderInterface \$builder, array \$options): void
    {
        \$builder
            ->add('name', TextType::class, [
                'label' => 'Name',
                'required' => true,
                'attr' => [
                    'class' => 'form-control',
                    'placeholder' => 'Enter name'
                ]
            ])
            ->add('description', TextareaType::class, [
                'label' => 'Description',
                'required' => false,
                'attr' => [
                    'class' => 'form-control',
                    'rows' => 4,
                    'placeholder' => 'Enter description'
                ]
            ])
            // Add more fields based on your entity
        ;
    }

    public function configureOptions(OptionsResolver \$resolver): void
    {
        \$resolver->setDefaults([
            'data_class' => $entityName::class,
        ]);
    }
}
";

// Generate Templates
$baseTemplate = "{% extends 'base.html.twig' %}

{% block title %}$entityName Management{% endblock %}

{% block body %}
<div class=\"container mt-4\">
    {% for label, messages in app.flashes %}
        {% for message in messages %}
            <div class=\"alert alert-{{ label }} alert-dismissible fade show\" role=\"alert\">
                {{ message }}
                <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>
            </div>
        {% endfor %}
    {% endfor %}
    
    {% block content %}{% endblock %}
</div>
{% endblock %}";

$indexTemplate = "{% extends '{$entityLower}/_base.html.twig' %}

{% block content %}
<div class=\"d-flex justify-content-between align-items-center mb-4\">
    <h1>{$entityName} List</h1>
    <a href=\"{{ path('{$entityLower}_new') }}\" class=\"btn btn-primary\">
        <i class=\"bi bi-plus-circle\"></i> New $entityName
    </a>
</div>

<div class=\"table-responsive\">
    <table class=\"table table-striped\">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for {$entityLower} in {$entityPlural} %}
            <tr>
                <td>{{ {$entityLower}.id }}</td>
                <td>{{ {$entityLower}.name|default('N/A') }}</td>
                <td>
                    <a href=\"{{ path('{$entityLower}_show', {'id': {$entityLower}.id}) }}\" class=\"btn btn-sm btn-info\">
                        <i class=\"bi bi-eye\"></i> View
                    </a>
                    <a href=\"{{ path('{$entityLower}_edit', {'id': {$entityLower}.id}) }}\" class=\"btn btn-sm btn-warning\">
                        <i class=\"bi bi-pencil\"></i> Edit
                    </a>
                    <form method=\"post\" action=\"{{ path('{$entityLower}_delete', {'id': {$entityLower}.id}) }}\" style=\"display:inline-block;\" onsubmit=\"return confirm('Are you sure?');\">
                        <input type=\"hidden\" name=\"_token\" value=\"{{ csrf_token('delete' ~ {$entityLower}.id) }}\">
                        <button class=\"btn btn-sm btn-danger\">
                            <i class=\"bi bi-trash\"></i> Delete
                        </button>
                    </form>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan=\"3\" class=\"text-center\">No {$entityPlural} found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}";

$newTemplate = "{% extends '{$entityLower}/_base.html.twig' %}

{% block content %}
<h1>Create New $entityName</h1>

<div class=\"card\">
    <div class=\"card-body\">
        {{ form_start(form) }}
            {{ form_widget(form) }}
            <div class=\"mt-3\">
                <button type=\"submit\" class=\"btn btn-success\">
                    <i class=\"bi bi-check-circle\"></i> Create
                </button>
                <a href=\"{{ path('{$entityLower}_index') }}\" class=\"btn btn-secondary\">
                    <i class=\"bi bi-arrow-left\"></i> Back to list
                </a>
            </div>
        {{ form_end(form) }}
    </div>
</div>
{% endblock %}";

$editTemplate = "{% extends '{$entityLower}/_base.html.twig' %}

{% block content %}
<h1>Edit $entityName</h1>

<div class=\"card\">
    <div class=\"card-body\">
        {{ form_start(form) }}
            {{ form_widget(form) }}
            <div class=\"mt-3\">
                <button type=\"submit\" class=\"btn btn-primary\">
                    <i class=\"bi bi-save\"></i> Update
                </button>
                <a href=\"{{ path('{$entityLower}_show', {'id': {$entityLower}.id}) }}\" class=\"btn btn-secondary\">
                    <i class=\"bi bi-arrow-left\"></i> Back
                </a>
            </div>
        {{ form_end(form) }}
    </div>
</div>

<div class=\"mt-3\">
    <form method=\"post\" action=\"{{ path('{$entityLower}_delete', {'id': {$entityLower}.id}) }}\" onsubmit=\"return confirm('Are you sure you want to delete this item?');\">
        <input type=\"hidden\" name=\"_token\" value=\"{{ csrf_token('delete' ~ {$entityLower}.id) }}\">
        <button class=\"btn btn-danger\">
            <i class=\"bi bi-trash\"></i> Delete this $entityName
        </button>
    </form>
</div>
{% endblock %}";

$showTemplate = "{% extends '{$entityLower}/_base.html.twig' %}

{% block content %}
<h1>$entityName Details</h1>

<div class=\"card\">
    <div class=\"card-body\">
        <table class=\"table\">
            <tbody>
                <tr>
                    <th>ID</th>
                    <td>{{ {$entityLower}.id }}</td>
                </tr>
                <tr>
                    <th>Name</th>
                    <td>{{ {$entityLower}.name|default('N/A') }}</td>
                </tr>
                <tr>
                    <th>Description</th>
                    <td>{{ {$entityLower}.description|default('N/A') }}</td>
                </tr>
                <!-- Add more fields as needed -->
            </tbody>
        </table>
    </div>
</div>

<div class=\"mt-3\">
    <a href=\"{{ path('{$entityLower}_edit', {'id': {$entityLower}.id}) }}\" class=\"btn btn-warning\">
        <i class=\"bi bi-pencil\"></i> Edit
    </a>
    <a href=\"{{ path('{$entityLower}_index') }}\" class=\"btn btn-secondary\">
        <i class=\"bi bi-arrow-left\"></i> Back to list
    </a>
</div>
{% endblock %}";

// Output the generated code
echo "===========================================\n";
echo "GENERATED SYMFONY CRUD FOR: $entityName\n";
echo "===========================================\n\n";

echo "1. CONTROLLER CODE:\n";
echo "-------------------\n";
echo $controllerCode;

echo "\n\n2. FORM TYPE CODE:\n";
echo "-------------------\n";
echo $formCode;

if (!$isApi) {
    echo "\n\n3. TEMPLATES:\n";
    echo "-------------------\n";
    echo "Base Template (templates/{$entityLower}/_base.html.twig):\n";
    echo $baseTemplate;
    echo "\n\n-------------------\n";
    echo "Index Template (templates/{$entityLower}/index.html.twig):\n";
    echo $indexTemplate;
    echo "\n\n-------------------\n";
    echo "New Template (templates/{$entityLower}/new.html.twig):\n";
    echo $newTemplate;
    echo "\n\n-------------------\n";
    echo "Edit Template (templates/{$entityLower}/edit.html.twig):\n";
    echo $editTemplate;
    echo "\n\n-------------------\n";
    echo "Show Template (templates/{$entityLower}/show.html.twig):\n";
    echo $showTemplate;
}

echo "\n\n===========================================\n";
echo "INSTALLATION INSTRUCTIONS:\n";
echo "===========================================\n";
echo "1. Save the controller to: src/Controller/" . ($isApi ? "Api/{$entityName}ApiController.php" : "{$entityName}Controller.php") . "\n";
echo "2. Save the form type to: src/Form/{$entityName}Type.php\n";
if (!$isApi) {
    echo "3. Create the template directory: mkdir -p templates/{$entityLower}\n";
    echo "4. Save each template to its respective file in templates/{$entityLower}/\n";
}
echo "\n";
echo "REQUIRED ENTITY SERIALIZATION GROUPS (for API):\n";
echo "Add these to your entity:\n";
echo "#[Groups(['{$entityLower}:read'])]\n";
echo "#[Groups(['{$entityLower}:write'])]\n";
echo "#[Groups(['{$entityLower}:detail'])]\n";
echo "\n";
echo "Don't forget to:\n";
echo "- Ensure your entity exists: src/Entity/$entityName.php\n";
echo "- Run migrations if needed: php bin/console doctrine:migrations:migrate\n";
echo "- Clear cache: php bin/console cache:clear\n";
