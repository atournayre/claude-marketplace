#!/usr/bin/env php
<?php
/**
 * Symfony Entity Generator Script
 * 
 * Usage: php generate-entity.php EntityName [field:type:options ...]
 * Example: php generate-entity.php Product name:string:255 price:decimal:10,2 category:relation:ManyToOne:Category
 */

if ($argc < 2) {
    echo "Usage: php generate-entity.php EntityName [field:type:options ...]\n";
    echo "Example: php generate-entity.php Product name:string:255 price:decimal:10,2\n";
    exit(1);
}

$entityName = $argv[1];
$fields = array_slice($argv, 2);

// Generate entity class
$entityCode = "<?php

namespace App\Entity;

use App\Repository\\{$entityName}Repository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: {$entityName}Repository::class)]
class $entityName
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int \$id = null;\n\n";

$gettersSetters = "\n    public function getId(): ?int
    {
        return \$this->id;
    }\n";

foreach ($fields as $fieldDefinition) {
    $parts = explode(':', $fieldDefinition);
    $fieldName = $parts[0] ?? '';
    $fieldType = $parts[1] ?? 'string';
    $fieldOptions = $parts[2] ?? '';
    
    if (empty($fieldName)) continue;
    
    // Handle different field types
    switch ($fieldType) {
        case 'string':
            $length = $fieldOptions ?: '255';
            $entityCode .= "    #[ORM\Column(length: $length)]
    #[Assert\NotBlank]
    #[Assert\Length(max: $length)]
    private ?string \$$fieldName = null;\n\n";
            
            $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?string
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(string \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'text':
            $entityCode .= "    #[ORM\Column(type: 'text')]
    private ?string \$$fieldName = null;\n\n";
            
            $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?string
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(?string \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'integer':
        case 'int':
            $entityCode .= "    #[ORM\Column]
    #[Assert\NotNull]
    private ?int \$$fieldName = null;\n\n";
            
            $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?int
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(int \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'decimal':
        case 'float':
            $precision = '10';
            $scale = '2';
            if ($fieldOptions) {
                $optionParts = explode(',', $fieldOptions);
                $precision = $optionParts[0] ?? '10';
                $scale = $optionParts[1] ?? '2';
            }
            $entityCode .= "    #[ORM\Column(type: 'decimal', precision: $precision, scale: $scale)]
    #[Assert\NotNull]
    private ?string \$$fieldName = null;\n\n";
            
            $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?string
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(string \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'boolean':
        case 'bool':
            $entityCode .= "    #[ORM\Column]
    private ?bool \$$fieldName = false;\n\n";
            
            $gettersSetters .= "\n    public function is" . ucfirst($fieldName) . "(): ?bool
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(bool \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'datetime':
            $entityCode .= "    #[ORM\Column(type: 'datetime_immutable')]
    private ?\\DateTimeImmutable \$$fieldName = null;\n\n";
            
            $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?\\DateTimeImmutable
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(\\DateTimeImmutable \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            break;
            
        case 'relation':
            $relationType = $parts[2] ?? 'ManyToOne';
            $targetEntity = $parts[3] ?? 'RelatedEntity';
            
            if ($relationType === 'ManyToOne') {
                $entityCode .= "    #[ORM\ManyToOne(inversedBy: '{$fieldName}s')]
    #[ORM\JoinColumn(nullable: false)]
    private ?$targetEntity \$$fieldName = null;\n\n";
                
                $gettersSetters .= "\n    public function get" . ucfirst($fieldName) . "(): ?$targetEntity
    {
        return \$this->$fieldName;
    }

    public function set" . ucfirst($fieldName) . "(?$targetEntity \$$fieldName): static
    {
        \$this->$fieldName = \$$fieldName;
        return \$this;
    }\n";
            } elseif ($relationType === 'OneToMany') {
                $entityCode = str_replace(
                    "use Doctrine\ORM\Mapping as ORM;",
                    "use Doctrine\Common\Collections\ArrayCollection;\nuse Doctrine\Common\Collections\Collection;\nuse Doctrine\ORM\Mapping as ORM;",
                    $entityCode
                );
                $entityCode .= "    #[ORM\OneToMany(mappedBy: '" . lcfirst($entityName) . "', targetEntity: $targetEntity::class)]
    private Collection \$$fieldName;\n\n";
                
                // Add constructor if not present
                if (!str_contains($gettersSetters, '__construct')) {
                    $gettersSetters .= "\n    public function __construct()
    {
        \$this->$fieldName = new ArrayCollection();
    }\n";
                }
                
                $gettersSetters .= "\n    /**
     * @return Collection<int, $targetEntity>
     */
    public function get" . ucfirst($fieldName) . "(): Collection
    {
        return \$this->$fieldName;
    }

    public function add" . ucfirst(rtrim($fieldName, 's')) . "($targetEntity \$" . rtrim($fieldName, 's') . "): static
    {
        if (!\$this->{$fieldName}->contains(\$" . rtrim($fieldName, 's') . ")) {
            \$this->{$fieldName}->add(\$" . rtrim($fieldName, 's') . ");
            \$" . rtrim($fieldName, 's') . "->set" . $entityName . "(\$this);
        }
        return \$this;
    }

    public function remove" . ucfirst(rtrim($fieldName, 's')) . "($targetEntity \$" . rtrim($fieldName, 's') . "): static
    {
        if (\$this->{$fieldName}->removeElement(\$" . rtrim($fieldName, 's') . ")) {
            if (\$" . rtrim($fieldName, 's') . "->get" . $entityName . "() === \$this) {
                \$" . rtrim($fieldName, 's') . "->set" . $entityName . "(null);
            }
        }
        return \$this;
    }\n";
            }
            break;
    }
}

$entityCode .= $gettersSetters;
$entityCode .= "}\n";

// Generate repository class
$repositoryCode = "<?php

namespace App\Repository;

use App\Entity\\$entityName;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<$entityName>
 *
 * @method $entityName|null find(\$id, \$lockMode = null, \$lockVersion = null)
 * @method $entityName|null findOneBy(array \$criteria, array \$orderBy = null)
 * @method {$entityName}[]    findAll()
 * @method {$entityName}[]    findBy(array \$criteria, array \$orderBy = null, \$limit = null, \$offset = null)
 */
class {$entityName}Repository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry \$registry)
    {
        parent::__construct(\$registry, $entityName::class);
    }

    public function save($entityName \$entity, bool \$flush = false): void
    {
        \$this->getEntityManager()->persist(\$entity);

        if (\$flush) {
            \$this->getEntityManager()->flush();
        }
    }

    public function remove($entityName \$entity, bool \$flush = false): void
    {
        \$this->getEntityManager()->remove(\$entity);

        if (\$flush) {
            \$this->getEntityManager()->flush();
        }
    }

    // Example custom query methods:
    
    /**
     * Find published {$entityName}s ordered by creation date
     *
     * @return {$entityName}[]
     */
    public function findPublishedOrderedByDate(): array
    {
        return \$this->createQueryBuilder('e')
            ->andWhere('e.published = :published')
            ->setParameter('published', true)
            ->orderBy('e.createdAt', 'DESC')
            ->getQuery()
            ->getResult();
    }

    /**
     * Find {$entityName}s by search term
     *
     * @return {$entityName}[]
     */
    public function findBySearchTerm(string \$term): array
    {
        return \$this->createQueryBuilder('e')
            ->andWhere('e.name LIKE :term OR e.description LIKE :term')
            ->setParameter('term', '%' . \$term . '%')
            ->orderBy('e.name', 'ASC')
            ->getQuery()
            ->getResult();
    }
}
";

echo "Generated Entity Code:\n";
echo "======================\n";
echo $entityCode;
echo "\n\nGenerated Repository Code:\n";
echo "==========================\n";
echo $repositoryCode;

echo "\n\nTo use this code:\n";
echo "1. Save the entity code to: src/Entity/$entityName.php\n";
echo "2. Save the repository code to: src/Repository/{$entityName}Repository.php\n";
echo "3. Run: php bin/console make:migration\n";
echo "4. Run: php bin/console doctrine:migrations:migrate\n";
